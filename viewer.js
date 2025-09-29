// Global variables to store experiment data
let resolvedData = [];
let conceptualData = [];
let currentTrialSequence = []; // Pre-generated trial sequence for selected experiment

// Utility to coerce CSV-style numeric fields into numbers
function parseNumeric(value) {
    if (value === null || value === undefined) {
        return null;
    }

    if (typeof value === 'number') {
        return Number.isFinite(value) ? value : null;
    }

    if (typeof value === 'string') {
        const trimmed = value.trim();
        if (trimmed === '' || trimmed.toLowerCase() === 'n/a') {
            return null;
        }
        const numeric = Number(trimmed);
        return Number.isFinite(numeric) ? numeric : null;
    }

    return null;
}

// Parse distribution parameters that may arrive as JSON-encoded strings
function getDistributionParams(rawValue) {
    if (!rawValue || rawValue === '[]') {
        return { values: [] };
    }

    try {
        const parsed = typeof rawValue === 'string' ? JSON.parse(rawValue) : rawValue;
        const arrayValues = Array.isArray(parsed) ? parsed : [];
        const numericValues = arrayValues
            .map(parseNumeric)
            .filter(value => value !== null);
        return { values: numericValues };
    } catch (error) {
        return { values: [], error };
    }
}

// Resolve a sensible static SOA fallback from condition metadata
function resolveStaticSOA(condition, explicitBase) {
    const candidates = [
        explicitBase,
        condition['Inter-task SOA'],
        condition['SOA'],
        condition.SOA
    ];

    for (const candidate of candidates) {
        const numeric = parseNumeric(candidate);
        if (numeric !== null) {
            return numeric;
        }
    }

    return 0;
}

// CSV parser using Papa Parse library
function parseCSV(csvText) {
    const result = Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.trim() // Clean up header names
    });
    
    if (result.errors.length > 0) {
        console.warn('CSV parsing errors:', result.errors);
    }
    
    return result.data;
}

// Convert absolute timing data to super-experiment parameters
function convertAbsoluteToSEParams(absoluteRow) {
    const seParams = {};
    
    // Determine if this is a dual-task condition based on available data
    // Check if both cue2 and go2 have meaningful durations (indicators of second task)
    const cue2Duration = parseInt(absoluteRow.effective_end_cue2) - parseInt(absoluteRow.effective_start_cue2);
    const go2Duration = parseInt(absoluteRow.effective_end_go2) - parseInt(absoluteRow.effective_start_go2);
    const isDualTask = cue2Duration > 0 && go2Duration > 0;
    
    // STEP 1: Determine task assignment to channels
    seParams.task_1 = 'mov';  // Channel 1 always gets movement task
    seParams.task_2 = isDualTask ? 'or' : null;   // Channel 2 gets orientation task only for dual-task
    
    // STEP 2: Convert cue and go signal timings (channel control signals)
    seParams.start_1 = parseInt(absoluteRow.effective_start_cue1);
    seParams.dur_1 = parseInt(absoluteRow.effective_end_cue1) - parseInt(absoluteRow.effective_start_cue1);
    seParams.start_2 = parseInt(absoluteRow.effective_start_cue2);
    seParams.dur_2 = parseInt(absoluteRow.effective_end_cue2) - parseInt(absoluteRow.effective_start_cue2);
    
    seParams.start_go_1 = parseInt(absoluteRow.effective_start_go1);
    seParams.dur_go_1 = parseInt(absoluteRow.effective_end_go1) - parseInt(absoluteRow.effective_start_go1);
    seParams.start_go_2 = parseInt(absoluteRow.effective_start_go2);
    seParams.dur_go_2 = parseInt(absoluteRow.effective_end_go2) - parseInt(absoluteRow.effective_start_go2);
    
    // STEP 3: Calculate raw stimulus timings from the correct pathways
    const mov_start = parseInt(absoluteRow.effective_start_stim1_mov);
    const mov_end = parseInt(absoluteRow.effective_end_stim1_mov);
    const mov_duration = mov_end - mov_start;
    
    // For dual-task, orientation task should come from Channel 2 (stim2_or)
    // For single-task, orientation distractor comes from Channel 1 (stim1_or)
    let or_start, or_end, or_duration;
    if (isDualTask) {
        or_start = parseInt(absoluteRow.effective_start_stim2_or);
        or_end = parseInt(absoluteRow.effective_end_stim2_or);
        or_duration = or_end - or_start;
    } else {
        or_start = parseInt(absoluteRow.effective_start_stim1_or);
        or_end = parseInt(absoluteRow.effective_end_stim1_or);
        or_duration = or_end - or_start;
    }
    
    // STEP 4: Assign stimulus pathways based on paradigm type
    if (isDualTask) {
        // DUAL-TASK: Task 1 (mov) goes to Channel 1, Task 2 (or) goes to Channel 2
        // Each channel gets its primary stimulus, and potentially distractors based on valency
        
        // Channel 1 (movement task): Primary movement stimulus (absolute timing)
        seParams.start_mov_1 = mov_start;
        seParams.dur_mov_1 = mov_duration;
        
        // Channel 2 (orientation task): Primary orientation stimulus (RELATIVE timing)
        // According to trial.js: or2Interval.addTime(or1Interval.end)
        // So start_or_2 should be: effective_start_stim2_or - effective_end_stim1_or
        const or1_start = parseInt(absoluteRow.effective_start_stim1_or);
        const or1_end = parseInt(absoluteRow.effective_end_stim1_or);
        seParams.start_or_2 = or_start - or1_end; // Relative to Channel 1 orientation end
        seParams.dur_or_2 = or_duration;
        
        // For dual-task, check if we need distractors (bivalent stimuli)
        // This is a simplified approach - in reality, you'd check stimulus valency per channel
        // For now, assume univalent stimuli in dual-task (no cross-channel distractors)
        seParams.start_or_1 = 0;
        seParams.dur_or_1 = 0;
        
        // Movement pathway on Channel 2 (if needed, also relative)
        // According to trial.js: mov2Interval.addTime(mov1Interval.end)
        const mov2_start = parseInt(absoluteRow.effective_start_stim2_mov);
        const mov2_end = parseInt(absoluteRow.effective_end_stim2_mov);
        if (mov2_end > mov2_start) {
            seParams.start_mov_2 = mov2_start - mov_end; // Relative to Channel 1 movement end
            seParams.dur_mov_2 = mov2_end - mov2_start;
        } else {
            seParams.start_mov_2 = 0;
            seParams.dur_mov_2 = 0;
        }
        
    } else {
        // SINGLE-TASK: Only Channel 1 is used, Channel 2 is completely inactive
        
        // Channel 1 gets the primary task stimulus
        seParams.start_mov_1 = mov_start;
        seParams.dur_mov_1 = mov_duration;
        
        // For single-task, stimulus valency determines if we need distractors on Channel 1
        // Use explicit stimulus valency metadata if available
        const stimulusValency = absoluteRow.Stimulus_Valency || 'Univalent';
        
        if (stimulusValency.includes('Bivalent') && or_duration > 0) {
            // Bivalent stimulus: activate orientation pathway on Channel 1 as distractor
            seParams.start_or_1 = or_start;
            seParams.dur_or_1 = or_duration;
        } else {
            // Univalent stimulus: only movement pathway active
            seParams.start_or_1 = 0;
            seParams.dur_or_1 = 0;
        }
        
        // Channel 2 completely inactive for single-task
        seParams.start_mov_2 = 0;
        seParams.dur_mov_2 = 0;
        seParams.start_or_2 = 0;
        seParams.dur_or_2 = 0;
    }
    
    // STEP 5: Set stimulus parameters (coherence)
    seParams.coh_1 = parseFloat(absoluteRow.coh_1);
    seParams.coh_2 = parseFloat(absoluteRow.coh_2);
    
    // Map coherence to specific pathways
    seParams.coh_mov_1 = seParams.dur_mov_1 > 0 ? parseFloat(absoluteRow.coh_1) : 0;
    seParams.coh_or_1 = seParams.dur_or_1 > 0 ? parseFloat(absoluteRow.coh_2) : 0;
    seParams.coh_mov_2 = seParams.dur_mov_2 > 0 ? parseFloat(absoluteRow.coh_1) : 0;
    seParams.coh_or_2 = seParams.dur_or_2 > 0 ? parseFloat(absoluteRow.coh_2) : 0;
    
    // STEP 6: Set default directions for active pathways
    seParams.dir_mov_1 = seParams.dur_mov_1 > 0 ? (Math.random() < 0.5 ? 0 : 180) : 0;
    seParams.dir_or_1 = seParams.dur_or_1 > 0 ? (Math.random() < 0.5 ? 0 : 180) : 0;
    seParams.dir_mov_2 = seParams.dur_mov_2 > 0 ? (Math.random() < 0.5 ? 0 : 180) : 0;
    seParams.dir_or_2 = seParams.dur_or_2 > 0 ? (Math.random() < 0.5 ? 0 : 180) : 0;
    
    // STEP 7: Set key mappings and response configuration
    seParams.movementKeyMap = { 180: 'a', 0: 'd' };
    seParams.orientationKeyMap = { 180: 'a', 0: 'd' };
    seParams.responseSetRelationship = 'identical';

    const stimulusValencyRaw = (absoluteRow.Stimulus_Valency || '').toString();
    const valencyLower = stimulusValencyRaw.toLowerCase();
    let stimulusCongruency = 'neutral';

    if (valencyLower.includes('incongruent')) {
        stimulusCongruency = 'incongruent';
    } else if (valencyLower.includes('congruent')) {
        stimulusCongruency = 'congruent';
    } else if (valencyLower.includes('neutral')) {
        stimulusCongruency = 'neutral';
    } else if (valencyLower.includes('univalent')) {
        stimulusCongruency = 'univalent';
    }

    seParams.stimulusCongruency = stimulusCongruency;
    
    return seParams;
}

// Generate trial directions based on condition metadata and trial assignment
function generateTrialDirections(condition, trialAssignment) {
    // Parse condition properties
    const nTasks = condition.N_Tasks || 1;
    const stimulusValency = condition.Stimulus_Valency || 'Univalent';
    const responseSetOverlap = condition.Simplified_RSO || 'Identical';
    
    // Initialize all directions to null
    let dir_mov_1 = null, dir_or_1 = null, dir_mov_2 = null, dir_or_2 = null;
    
    if (nTasks == 2) {
        // DUAL-TASK: Both channels active
        // trialAssignment specifies which task goes to which channel
        
        const task1 = trialAssignment.channel1_task; // e.g., 'mov' or 'or'
        const task2 = trialAssignment.channel2_task; // e.g., 'or' or 'mov'
        
        // Assume univalent stimuli for dual-task (no cross-channel distractors)
        
        // Generate directions for active pathways
        if (task1 === 'mov') {
            dir_mov_1 = Math.random() < 0.5 ? 0 : 180;
        } else if (task1 === 'or') {
            dir_or_1 = Math.random() < 0.5 ? 0 : 180;
        }
        
        if (task2 === 'mov') {
            dir_mov_2 = Math.random() < 0.5 ? 0 : 180;
        } else if (task2 === 'or') {
            if (responseSetOverlap.includes('Disjoint')) {
                // Disjoint response sets: use orthogonal directions
                dir_or_2 = Math.random() < 0.5 ? 90 : 270;
            } else {
                // Identical response sets: use same response dimension 
                dir_or_2 = Math.random() < 0.5 ? 0 : 180;
            }
        }
        
    } else {
        // SINGLE-TASK (N_Tasks == 1): Only Channel 1 active
        // trialAssignment.currentTask determines which pathway is primary
        const currentTask = trialAssignment.currentTask;
        
        if (stimulusValency.includes('Univalent')) {
            // Only the primary pathway gets a direction
            if (currentTask === 'mov') {
                dir_mov_1 = Math.random() < 0.5 ? 0 : 180;
            } else if (currentTask === 'or') {
                dir_or_1 = Math.random() < 0.5 ? 0 : 180;
            }
            
        } else if (stimulusValency.includes('Bivalent')) {
            // Both pathways of Channel 1 get directions (target + distractor)
            
            let primary_dir, distractor_dir;
            
            if (stimulusValency.includes('Congruent')) {
                // Both stimuli should lead to same response
                primary_dir = Math.random() < 0.5 ? 0 : 180;
                distractor_dir = primary_dir; // Same direction for congruent
            } else if (stimulusValency.includes('Incongruent')) {
                // Stimuli should lead to opposite responses
                primary_dir = Math.random() < 0.5 ? 0 : 180;
                distractor_dir = primary_dir === 0 ? 180 : 0; // Opposite direction
            } else if (stimulusValency.includes('Neutral')) {
                // Neutral - stimuli should be orthogonal
                primary_dir = Math.random() < 0.5 ? 0 : 180; // left/right
                distractor_dir = Math.random() < 0.5 ? 90 : 270; // up/down
            } else {
                // Plain "Bivalent" without specification - random directions
                primary_dir = Math.random() < 0.5 ? 0 : 180;
                distractor_dir = Math.random() < 0.5 ? 0 : 180;
            }
            
            // Assign directions based on current task
            if (currentTask === 'mov') {
                dir_mov_1 = primary_dir;    // Movement is primary
                dir_or_1 = distractor_dir;  // Orientation is distractor
            } else if (currentTask === 'or') {
                dir_or_1 = primary_dir;     // Orientation is primary  
                dir_mov_1 = distractor_dir; // Movement is distractor
            }
        }
        
        // Channel 2 completely inactive for single-task
        // dir_mov_2 = null, dir_or_2 = null (already set above)
    }
    
    return { dir_mov_1, dir_or_1, dir_mov_2, dir_or_2 };
}

// Generate ITI for a trial based on distribution parameters (updated to use RSI column names)
function generateITI(condition) {
    const distributionType = condition.RSI_Distribution_Type || condition.ITI_Distribution_Type || 'fixed';
    const baseITIValue = parseNumeric(condition.ITI_ms);
    const fallbackITI = baseITIValue !== null ? baseITIValue : 1000;

    if (distributionType === 'fixed') {
        return fallbackITI;
    }

    const rawParams = condition.RSI_Distribution_Params || condition.ITI_Distribution_Params;
    const { values: params, error } = getDistributionParams(rawParams);

    if (error) {
        console.warn('Failed to parse RSI_Distribution_Params:', rawParams);
        return fallbackITI;
    }

    if (distributionType === 'uniform' && params.length >= 2) {
        const [rawMin, rawMax] = params;
        if (rawMin !== undefined && rawMax !== undefined) {
            const min = Math.min(rawMin, rawMax);
            const max = Math.max(rawMin, rawMax);
            return min + Math.random() * (max - min);
        }
    } else if (distributionType === 'choice' && params.length > 0) {
        return params[Math.floor(Math.random() * params.length)];
    }

    // Default to base ITI if distribution can't be processed
    return fallbackITI;
}

// Generate SOA for a trial based on distribution parameters
function generateSOA(condition, baseSoa) {
    const fallbackSOA = resolveStaticSOA(condition, baseSoa);
    const distributionType = condition.SOA_Distribution_Type || 'fixed';

    if (distributionType === 'fixed') {
        return fallbackSOA;
    }

    const { values: params, error } = getDistributionParams(condition.SOA_Distribution_Params);

    if (error) {
        console.warn('Failed to parse SOA_Distribution_Params:', condition.SOA_Distribution_Params);
        return fallbackSOA;
    }

    if (distributionType === 'uniform' && params.length >= 2) {
        const [rawMin, rawMax] = params;
        if (rawMin !== undefined && rawMax !== undefined) {
            const min = Math.min(rawMin, rawMax);
            const max = Math.max(rawMin, rawMax);
            return min + Math.random() * (max - min);
        }
    } else if (distributionType === 'choice' && params.length > 0) {
        return params[Math.floor(Math.random() * params.length)];
    }

    // Default to base SOA if distribution can't be processed
    return fallbackSOA;
}

// Generate task sequence for single-task paradigms
function generateTaskSequence(sequenceType, numTrials, switchRate) {
    const sequence = [];
    
    if (sequenceType === 'Random') {
        // Random sequence with specified switch rate
        let currentTask = 'mov'; // Start with movement task
        sequence.push(currentTask);
        
        for (let i = 1; i < numTrials; i++) {
            if (Math.random() < (switchRate / 100)) {
                // Switch task
                currentTask = currentTask === 'mov' ? 'or' : 'mov';
            }
            sequence.push(currentTask);
        }
    } else if (sequenceType === 'AABB') {
        // AABB pattern: mov, mov, or, or, mov, mov, or, or, ...
        for (let i = 0; i < numTrials; i++) {
            const blockIndex = Math.floor(i / 2) % 2;
            sequence.push(blockIndex === 0 ? 'mov' : 'or');
        }
    } else if (sequenceType === 'ABAB') {
        // ABAB pattern: mov, or, mov, or, ...
        for (let i = 0; i < numTrials; i++) {
            sequence.push(i % 2 === 0 ? 'mov' : 'or');
        }
    } else if (sequenceType === 'AAAABBBB') {
        // AAAABBBB pattern: mov, mov, mov, mov, or, or, or, or, ...
        for (let i = 0; i < numTrials; i++) {
            const blockIndex = Math.floor(i / 4) % 2;
            sequence.push(blockIndex === 0 ? 'mov' : 'or');
        }
    } else {
        // Default to alternating pattern
        for (let i = 0; i < numTrials; i++) {
            sequence.push(i % 2 === 0 ? 'mov' : 'or');
        }
    }
    
    return sequence;
}

// Generate task-to-channel assignment sequence for dual-task paradigms
function generateTaskAssignmentSequence(task1Type, task2Type, numTrials, switchRate) {
    const sequence = [];
    
    // Default assignment (switch rate = 0%)
    let channel1_task = task1Type;  // e.g., 'mov'
    let channel2_task = task2Type;  // e.g., 'or'
    
    for (let i = 0; i < numTrials; i++) {
        if (i === 0) {
            // First trial uses default assignment
            sequence.push({ channel1_task, channel2_task });
        } else {
            // Subsequent trials: check if we should switch assignment
            if (Math.random() < (switchRate / 100)) {
                // Switch the task-to-channel assignment
                [channel1_task, channel2_task] = [channel2_task, channel1_task];
            }
            sequence.push({ channel1_task, channel2_task });
        }
    }
    
    return sequence;
}

// Group conditions by Block_ID for block-aware trial generation
function groupByBlock(data) {
    const blocks = {};
    
    data.forEach(condition => {
        const blockId = condition.Block_ID || condition.Experiment; // Fall back to Experiment name if no Block_ID
        
        if (!blocks[blockId]) {
            blocks[blockId] = [];
        }
        blocks[blockId].push(condition);
    });
    
    return blocks;
}

// Helper function to extract viewer config from condition
function extractViewerConfig(condition) {
    let config = {};
    try {
        if (condition.viewer_config && condition.viewer_config !== '{}') {
            config = JSON.parse(condition.viewer_config);
        }
    } catch (e) {
        console.warn('Failed to parse viewer_config:', condition.viewer_config);
    }
    return config;
}

// Helper function to extract Super_Experiment_Mapping_Notes
function extractMappingNotes(condition) {
    let notes = {};
    try {
        if (condition.Super_Experiment_Mapping_Notes && condition.Super_Experiment_Mapping_Notes !== '{}') {
            notes = JSON.parse(condition.Super_Experiment_Mapping_Notes);
        }
    } catch (e) {
        console.warn('Failed to parse Super_Experiment_Mapping_Notes:', condition.Super_Experiment_Mapping_Notes);
    }
    return notes;
}

// Generate dynamic SOA from viewer config in mapping notes
function generateDynamicSOA(condition) {
    const mappingNotes = extractMappingNotes(condition);
    const viewerConfig = mappingNotes.viewer_config || {};
    
    if (viewerConfig.SOA_distribution === 'choice' && viewerConfig.SOA_values) {
        // Sample from discrete distribution
        const values = (Array.isArray(viewerConfig.SOA_values) ? viewerConfig.SOA_values : [])
            .map(parseNumeric)
            .filter(value => value !== null);
        if (values.length > 0) {
            return values[Math.floor(Math.random() * values.length)];
        }
    } else if (viewerConfig.SOA_distribution === 'uniform' && viewerConfig.SOA_range) {
        // Sample from uniform distribution
        const range = Array.isArray(viewerConfig.SOA_range) ? viewerConfig.SOA_range : [];
        const minValue = parseNumeric(range[0]);
        const maxValue = parseNumeric(range[1]);

        if (minValue !== null && maxValue !== null) {
            const min = Math.min(minValue, maxValue);
            const max = Math.max(minValue, maxValue);
            return min + Math.random() * (max - min);
        }
    }
    
    // Fallback to existing SOA generation logic
    return generateSOA(condition);
}

// Recalculate absolute timings based on dynamic SOA
function recalculateTimingsWithDynamicSOA(condition, dynamicSOA) {
    const modifiedCondition = { ...condition };
    
    // For dual-task experiments, we need to recalculate T2 timings based on dynamic SOA
    const nTasks = parseInt(condition.N_Tasks, 10) || 1;
    const soaValue = parseNumeric(dynamicSOA);

    if (nTasks === 2 && soaValue !== null) {
        // Get T1 stimulus timing (baseline)
        const t1_stim_start = parseInt(condition.effective_start_stim1_mov) || 0;
        
        // Calculate new T2 stimulus timing: T1_start + dynamic_SOA
        const t2_stim_start = t1_stim_start + soaValue;
        const t2_stim_duration = (parseInt(condition.effective_end_stim2_or) || 0) - (parseInt(condition.effective_start_stim2_or) || 0);
        const t2_stim_end = t2_stim_start + t2_stim_duration;
        
        // Update T2 stimulus timings
        modifiedCondition.effective_start_stim2_or = t2_stim_start.toString();
        modifiedCondition.effective_end_stim2_or = t2_stim_end.toString();
        
        // Calculate T2 cue timing based on CSI
        const t2_csi = parseInt(condition['Task 2 CSI']) || 0;
        
        if (t2_csi > 0) {
            // When CSI > 0, calculate cue duration from original data
            const t2_cue_duration = (parseInt(condition.effective_end_cue2) || 0) - (parseInt(condition.effective_start_cue2) || 0);
            
            // T2 cue starts CSI ms before T2 stimulus
            const t2_cue_start = t2_stim_start - t2_csi;
            const t2_cue_end = t2_cue_start + t2_cue_duration;
            
            modifiedCondition.effective_start_cue2 = t2_cue_start.toString();
            modifiedCondition.effective_end_cue2 = t2_cue_end.toString();
        } else {
            // When CSI is 0, cue and stimulus start simultaneously with stimulus duration
            modifiedCondition.effective_start_cue2 = t2_stim_start.toString();
            modifiedCondition.effective_end_cue2 = t2_stim_end.toString();
        }
        
        // Update go signal timing to match stimulus
        modifiedCondition.effective_start_go2 = t2_stim_start.toString();
        modifiedCondition.effective_end_go2 = t2_stim_end.toString();
    }
    
    return modifiedCondition;
}

// Helper function to determine trial transition type based on sequence position
function getTrialTransitionType(trialIndex, taskSequence) {
    if (trialIndex === 0) {
        return 'Pure'; // First trial is always pure
    }
    
    const currentTask = taskSequence[trialIndex];
    const previousTask = taskSequence[trialIndex - 1];
    
    if (currentTask === previousTask) {
        return 'Repeat';
    } else {
        return 'Switch';
    }
}

// Advanced trial sequence generation - now supports both single conditions and blocks
function createTrialSequence(conditionOrBlock, numTrials = 10) {
    const trialSequence = [];
    
    // Determine if we're dealing with a single condition or a block (array of conditions)
    const isBlock = Array.isArray(conditionOrBlock);
    const conditions = isBlock ? conditionOrBlock : [conditionOrBlock];
    const primaryCondition = conditions[0]; // Use first condition for primary parameters
    
    // A. Determine Sequence Order - ALWAYS use primary condition's configuration
    let sequenceType = primaryCondition.Sequence_Type || 'Random';
    let switchRate = parseFloat(primaryCondition.Switch_Rate_Percent) || 0;
    
    // Check for sequence type override in viewer_config from PRIMARY CONDITION ONLY
    // This enforces the "Primary Condition" rule - ignore viewer_config from other conditions
    const primaryViewerConfig = extractViewerConfig(primaryCondition);
    if (primaryViewerConfig.sequence_type) {
        sequenceType = primaryViewerConfig.sequence_type;
    }
    
    // Determine paradigm type from N_Tasks
    const nTasks = primaryCondition.N_Tasks || 1;
    const isDualTask = (nTasks == 2);
    
    // Generate task sequence based on paradigm type and sequence rules
    let taskSequence;
    
    if (isDualTask) {
        // DUAL-TASK: Generate task-to-channel assignments using switch rate
        // For now, keep existing dual-task logic (can be enhanced later for blocks)
        const assignmentSequence = generateTaskAssignmentSequence(
            'mov',  // Always map Task 1 to movement
            'or',   // Always map Task 2 to orientation 
            numTrials, 
            switchRate
        );
        taskSequence = assignmentSequence.map(assignment => `${assignment.channel1_task}+${assignment.channel2_task}`);
    } else {
        // SINGLE-TASK: Generate task sequence using sequence type
        const rawTaskSequence = generateTaskSequence(sequenceType, numTrials, switchRate);
        taskSequence = rawTaskSequence;
    }
    
    // Generate trials
    for (let i = 0; i < numTrials; i++) {
        // B. Map Trial to Condition: Determine transition type for this trial
        const transitionType = getTrialTransitionType(i, taskSequence);
        
        // C. Find the specific condition row that matches this trial's transition type
        let selectedCondition = primaryCondition; // Default fallback
        
        if (isBlock) {
            // Look for a condition with matching Trial_Transition_Type
            const matchingCondition = conditions.find(cond => 
                cond.Trial_Transition_Type === transitionType
            );
            if (matchingCondition) {
                selectedCondition = matchingCondition;
            }
        }
        
        // D. Generate Dynamic Values: SOA and ITI for this specific trial
        const dynamicSOA = generateDynamicSOA(selectedCondition);
        const dynamicITI = generateITI(selectedCondition);
        
        // Recalculate absolute timings with dynamic SOA
        const recalculatedCondition = recalculateTimingsWithDynamicSOA(selectedCondition, dynamicSOA);
        
        // Generate trial assignment and directions
        let assignment;
        if (isDualTask) {
            // Parse the combined task assignment (e.g., "mov+or")
            const [task1, task2] = taskSequence[i].split('+');
            assignment = { channel1_task: task1, channel2_task: task2 };
        } else {
            assignment = { currentTask: taskSequence[i] };
        }
        
        const directions = generateTrialDirections(selectedCondition, assignment);
        
        // Get base parameters from the recalculated condition with dynamic SOA
        const baseParams = convertAbsoluteToSEParams(recalculatedCondition);
        
        let trialParams;
        
        if (isDualTask) {
            // DUAL-TASK: Both channels active, task assignment may vary per trial
            trialParams = {
                ...baseParams,
                task_1: assignment.channel1_task,
                task_2: assignment.channel2_task,
                
                // Apply generated directions to all four pathways
                dir_mov_1: directions.dir_mov_1 || 0,
                dir_or_1: directions.dir_or_1 || 0,
                dir_mov_2: directions.dir_mov_2 || 0,
                dir_or_2: directions.dir_or_2 || 0,
            };
            
        } else {
            // SINGLE-TASK: Only Channel 1 active, task_1 varies
            trialParams = {
                ...baseParams,
                task_1: assignment.currentTask,  
                task_2: null,                    
                
                // Apply generated directions
                dir_mov_1: directions.dir_mov_1 || 0,
                dir_or_1: directions.dir_or_1 || 0,
                dir_mov_2: 0,  
                dir_or_2: 0,   
                
                // Ensure Channel 2 is completely inactive
                start_2: 0,
                dur_2: 0,
                start_go_2: 0,
                dur_go_2: 0,
                start_mov_2: 0,
                dur_mov_2: 0,
                start_or_2: 0,
                dur_or_2: 0,
                coh_mov_2: 0,
                coh_or_2: 0,
            };
        }
        
        trialSequence.push({
            seParams: trialParams,
            regenTime: dynamicITI,
            trialNumber: i + 1,
            taskType: isDualTask ? `${assignment.channel1_task}+${assignment.channel2_task}` : assignment.currentTask,
            transitionType: transitionType, // Add transition type for testing
            selectedCondition: selectedCondition.Experiment, // Add selected condition for testing
            dynamicSOA: dynamicSOA // Add dynamic SOA for testing
        });
    }
    
    return trialSequence;
}

// Helper function to safely add info panel rows using DOM construction
function addInfoRow(container, label, value) {
    const dt = document.createElement('dt');
    dt.textContent = label;
    
    const dd = document.createElement('dd');
    dd.textContent = value ?? 'N/A';
    
    container.append(dt, dd);
}

// Update info panel with experiment details
function updateInfoPanel(conceptualRow) {
    const infoPanel = document.getElementById('info-panel');
    
    if (!conceptualRow) {
        infoPanel.innerHTML = '<div class="error">Experiment data not found</div>';
        return;
    }
    
    // Helper function to safely get column values with fallbacks
    const getValue = (primary, fallback) => {
        const value = conceptualRow[primary] || conceptualRow[fallback];
        return (value && value !== 'undefined' && value.trim() !== '') ? value : 'N/A';
    };
    
    // Get SOA value - check for distribution first, then fallback to static value
    let soaDisplay = 'N/A';

    const formatStaticSOA = () => {
        const staticCandidate = getValue('Inter-task SOA', 'SOA');
        const numericValue = parseNumeric(staticCandidate);

        if (numericValue !== null) {
            return `${numericValue} ms`;
        }
        return staticCandidate !== 'N/A' ? staticCandidate : 'N/A';
    };

    try {
        const mappingNotes = extractMappingNotes(conceptualRow);
        const viewerConfig = mappingNotes.viewer_config || {};

        if (viewerConfig.SOA_distribution === 'choice' && viewerConfig.SOA_values) {
            const values = (Array.isArray(viewerConfig.SOA_values) ? viewerConfig.SOA_values : [])
                .map(parseNumeric)
                .filter(value => value !== null);

            if (values.length > 0) {
                soaDisplay = `Choice from [${values.join(', ')}] ms`;
            } else {
                soaDisplay = formatStaticSOA();
            }
        } else if (viewerConfig.SOA_distribution === 'uniform' && viewerConfig.SOA_range) {
            const range = Array.isArray(viewerConfig.SOA_range) ? viewerConfig.SOA_range : [];
            const min = parseNumeric(range[0]);
            const max = parseNumeric(range[1]);

            if (min !== null && max !== null) {
                const low = Math.min(min, max);
                const high = Math.max(min, max);
                soaDisplay = `Uniform(${low}, ${high}) ms`;
            } else {
                soaDisplay = formatStaticSOA();
            }
        } else {
            soaDisplay = formatStaticSOA();
        }
    } catch (e) {
        // If extractMappingNotes fails, fallback to static SOA value
        soaDisplay = formatStaticSOA();
    }
    
    // Clear and rebuild info panel using DOM construction
    infoPanel.innerHTML = '';
    
    // Create header
    const header = document.createElement('h3');
    header.textContent = 'Experiment Details';
    infoPanel.appendChild(header);
    
    // Create definition list for organized layout
    const dl = document.createElement('dl');
    
    const numTasks = parseInt(getValue('Number of Tasks', 'N_Tasks')) || 1;
    const task1SRM = getValue('Task 1 Stimulus-Response Mapping', 'SRM_1');
    const task2SRM = getValue('Task 2 Stimulus-Response Mapping', 'SRM_2');
    
    // Add experiment info rows
    addInfoRow(dl, 'Experiment', getValue('Experiment', ''));
    addInfoRow(dl, 'Number of Tasks', numTasks.toString());
    addInfoRow(dl, 'SOA', soaDisplay);
    addInfoRow(dl, 'Task 1 Type', getValue('Task 1 Type', ''));
    
    if (numTasks > 1) {
        addInfoRow(dl, 'Task 2 Type', getValue('Task 2 Type', ''));
    }
    
    addInfoRow(dl, 'Stimulus Valency', getValue('Stimulus Valency', ''));
    addInfoRow(dl, 'Response Set Overlap', getValue('Response Set Overlap', 'Simplified_RSO'));
    
    // Add SRM info based on number of tasks
    if (numTasks === 1) {
        addInfoRow(dl, 'Stimulus Response Mapping', task1SRM);
    } else {
        addInfoRow(dl, 'Task 1 SRM', task1SRM);
        addInfoRow(dl, 'Task 2 SRM', task2SRM);
    }
    
    const switchRate = getValue('Switch Rate', 'Switch_Rate_Percent');
    addInfoRow(dl, 'Switch Rate', switchRate !== 'N/A' ? `${switchRate}%` : switchRate);
    addInfoRow(dl, 'Notes', getValue('Notes', '') || 'N/A');
    
    infoPanel.appendChild(dl);
}

// Color token map for timeline elements
const TIMELINE_COLORS = {
    get cue() { return getComputedStyle(document.documentElement).getPropertyValue('--cue').trim(); },
    get stimPrimary() { return getComputedStyle(document.documentElement).getPropertyValue('--stim-primary').trim(); },
    get stimDistractor() { return getComputedStyle(document.documentElement).getPropertyValue('--stim-distractor').trim(); },
    get go() { return getComputedStyle(document.documentElement).getPropertyValue('--go').trim(); }
};

// Create or update timeline legend
function updateTimelineLegend(isDualTask) {
    const legend = document.getElementById('timeline-legend');
    if (!legend) return;
    
    // Clear existing legend
    legend.innerHTML = '';
    
    // Define legend items based on timeline content
    const legendItems = [
        { color: TIMELINE_COLORS.cue, label: 'Cue' },
        { color: TIMELINE_COLORS.stimPrimary, label: 'Stimulus (Primary)' },
        { color: TIMELINE_COLORS.stimDistractor, label: 'Stimulus (Distractor)' }
    ];
    
    if (isDualTask) {
        legendItems.push({ color: TIMELINE_COLORS.go, label: 'T2 Cue' });
    }
    
    // Create legend items
    legendItems.forEach(({ color, label }) => {
        const item = document.createElement('div');
        item.className = 'legend-item';
        
        const swatch = document.createElement('div');
        swatch.className = 'legend-swatch';
        swatch.style.backgroundColor = color;
        
        const text = document.createElement('span');
        text.textContent = label;
        
        item.appendChild(swatch);
        item.appendChild(text);
        legend.appendChild(item);
    });
    
    // Show legend
    legend.style.display = 'flex';
}

// Draw timeline visualization from trial-specific data
function drawTimeline(trialData) {
    const svg = document.getElementById('timeline-svg');
    
    if (!trialData) {
        setSvgMessage(svg, 'No trial data available', 'error');
        // Hide legend when no data
        const legend = document.getElementById('timeline-legend');
        if (legend) legend.style.display = 'none';
        return;
    }
    
    // Note: Timeline needs to redraw for each trial as parameters can vary
    // Only skip if we have the exact same data structure (rare case)
    const essentialProps = [
        'task_1', 'task_2', 'start_1', 'dur_1', 'start_2', 'dur_2',
        'start_mov_1', 'dur_mov_1', 'start_or_1', 'dur_or_1',
        'start_mov_2', 'dur_mov_2', 'start_or_2', 'dur_or_2'
    ];
    
    const trialKey = essentialProps.map(prop => `${prop}:${trialData[prop] || 0}`).join('|');
    
    // Minor optimization: skip redraw only if timeline structure is identical
    const currentKey = svg.getAttribute('data-trial-key');
    if (currentKey === trialKey) {
        return;
    }
    
    svg.setAttribute('data-trial-key', trialKey);
    
    // Clear any existing content first
    svg.innerHTML = '';
    
    // Calculate timeline end time from trial data
    const timelineEnd = Math.max(
        (trialData.start_mov_1 || 0) + (trialData.dur_mov_1 || 0),
        (trialData.start_or_1 || 0) + (trialData.dur_or_1 || 0),
        (trialData.start_mov_2 || 0) + (trialData.dur_mov_2 || 0),
        (trialData.start_or_2 || 0) + (trialData.dur_or_2 || 0),
        (trialData.start_1 || 0) + (trialData.dur_1 || 0),
        (trialData.start_2 || 0) + (trialData.dur_2 || 0),
        (trialData.start_go_1 || 0) + (trialData.dur_go_1 || 0),
        (trialData.start_go_2 || 0) + (trialData.dur_go_2 || 0)
    ) + (trialData.regenTime || 500); // Add ITI and padding
    
    const margin = { left: 120, right: 20, top: 20, bottom: 30 };
    const width = svg.clientWidth - margin.left - margin.right;
    const height = 260;
    
    // Add shadow filter definition
    let defs = svg.querySelector('defs');
    if (!defs) {
        defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        const filter = document.createElementNS("http://www.w3.org/2000/svg", "filter");
        filter.setAttribute("id", "softShadow");
        filter.setAttribute("x", "-20%");
        filter.setAttribute("y", "-20%");
        filter.setAttribute("width", "140%");
        filter.setAttribute("height", "140%");
        
        const feDropShadow = document.createElementNS("http://www.w3.org/2000/svg", "feDropShadow");
        feDropShadow.setAttribute("dx", "0");
        feDropShadow.setAttribute("dy", "2");
        feDropShadow.setAttribute("stdDeviation", "2");
        feDropShadow.setAttribute("flood-opacity", "0.1");
        
        filter.appendChild(feDropShadow);
        defs.appendChild(filter);
        svg.appendChild(defs);
    }

    // Create or get persistent static layer (ruler/grid/axis)
    let ruler = svg.querySelector('#ruler');
    if (!ruler) {
        ruler = document.createElementNS("http://www.w3.org/2000/svg", "g");
        ruler.id = 'ruler';
        ruler.setAttribute("transform", `translate(${margin.left},${margin.top})`);
        svg.appendChild(ruler);
    }
    
    // Create or clear dynamic layer (bars)
    let bars = svg.querySelector('#bars');
    if (bars) {
        bars.replaceChildren();
    } else {
        bars = document.createElementNS("http://www.w3.org/2000/svg", "g");
        bars.id = 'bars';
        bars.setAttribute("transform", `translate(${margin.left},${margin.top})`);
        svg.appendChild(bars);
    }
    
    // Use ruler group for static elements, bars group for dynamic elements
    const g = ruler;  // Static elements
    const barsGroup = bars;  // Dynamic elements
    
    // Only redraw static elements if ruler is empty (first time or timeline dimensions changed)
    if (ruler.children.length === 0 || ruler.getAttribute('data-timeline-end') !== timelineEnd.toString()) {
        ruler.replaceChildren(); // Clear if dimensions changed
        ruler.setAttribute('data-timeline-end', timelineEnd.toString());
        
        // Draw vertical grid lines
        for (let t = 0; t <= timelineEnd; t += 250) {
            const x = (t * width / timelineEnd);
            const grid = document.createElementNS("http://www.w3.org/2000/svg", "line");
            grid.setAttribute("x1", x);
            grid.setAttribute("x2", x);
            grid.setAttribute("y1", 0);
            grid.setAttribute("y2", height);
            grid.setAttribute("stroke", "currentColor");
            grid.setAttribute("opacity", t % 1000 === 0 ? "0.18" : "0.08");
            grid.setAttribute("class", t % 1000 === 0 ? "timeline-grid major" : "timeline-grid");
            ruler.appendChild(grid);
        }

        // Draw time axis
        const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
        axis.setAttribute("x1", "0");
        axis.setAttribute("y1", height);
        axis.setAttribute("x2", width);
        axis.setAttribute("y2", height);
        axis.setAttribute("stroke", "currentColor");
        axis.setAttribute("stroke-width", "2");
        axis.setAttribute("opacity", "0.3");
        ruler.appendChild(axis);
        
        // Add time markers
        const tickInterval = Math.ceil(timelineEnd / 8000) * 1000; // Dynamic tick interval
        for(let t = 0; t <= timelineEnd; t += tickInterval) {
            const x = (t * width / timelineEnd);
            
            // Tick mark
            const tick = document.createElementNS("http://www.w3.org/2000/svg", "line");
            tick.setAttribute("x1", x);
            tick.setAttribute("y1", height - 5);
            tick.setAttribute("x2", x);
            tick.setAttribute("y2", height + 5);
            tick.setAttribute("stroke", "currentColor");
            tick.setAttribute("stroke-width", "1");
            tick.setAttribute("opacity", "0.5");
            ruler.appendChild(tick);
            
            // Label
            const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
            label.setAttribute("x", x);
            label.setAttribute("y", height + 20);
            label.setAttribute("text-anchor", "middle");
            label.setAttribute("fill", "currentColor");
            label.setAttribute("font-size", "10px");
            label.setAttribute("class", "timeline-label");
            label.textContent = `${t}ms`;
            ruler.appendChild(label);
        }
        
        // Draw axis labels (static)
        const axisLabels = [
            { label: "T1 Cue", yPos: 30 },
            { label: "T1 Stimulus", yPos: 60 },
            { label: "T2 Cue", yPos: 120 },
            { label: "T2 Stimulus", yPos: 150 }
        ];
        
        axisLabels.forEach(({label, yPos}) => {
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", -10);
            text.setAttribute("y", yPos + 15);
            text.setAttribute("text-anchor", "end");
            text.setAttribute("fill", "currentColor");
            text.setAttribute("font-size", "12px");
            text.setAttribute("font-weight", "bold");
            text.setAttribute("class", "timeline-label");
            text.textContent = label;
            ruler.appendChild(text);
        });
    }
    
    // Define y-positions for the timeline elements
    const yPositions = {
        t1_cue: 30,
        t1_stim: 60,
        t2_cue: 120,
        t2_stim: 150
    };
    
    // Draw timeline components
    function drawComponent(startTime, endTime, yPos, color, label) {
        if (startTime >= endTime) return;
        
        const x = startTime * width / timelineEnd;
        const componentWidth = Math.max(2, (endTime - startTime) * width / timelineEnd);
        
        // Draw rectangle with rounded corners and shadow
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", yPos);
        rect.setAttribute("width", componentWidth);
        rect.setAttribute("height", "25");
        rect.setAttribute("rx", "6");
        rect.setAttribute("ry", "6");
        rect.setAttribute("fill", color);
        rect.setAttribute("opacity", "0.8");
        rect.setAttribute("filter", "url(#softShadow)");
        rect.setAttribute("class", "timeline-bar");
        barsGroup.appendChild(rect);
        
        // Add timing labels directly on the bars for better readability
        if (componentWidth > 40) {
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", x + componentWidth/2);
            text.setAttribute("y", yPos + 17); // Centered vertically in the 25px high bar
            text.setAttribute("text-anchor", "middle");
            text.setAttribute("fill", "white");
            text.setAttribute("font-size", "9px");
            text.setAttribute("font-weight", "bold");
            text.setAttribute("text-shadow", "0 1px 2px rgba(0,0,0,0.8)"); // Better contrast
            text.textContent = `${startTime}-${endTime}ms`;
            barsGroup.appendChild(text);
        }
        
        // Add hover tooltip for detailed information
        const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
        title.textContent = `${label}: ${startTime}ms - ${endTime}ms (Duration: ${endTime - startTime}ms)`;
        rect.appendChild(title);
    }
    
    // Determine what to draw based on actual trial structure (guard against undefined/null)
    const isDualTask = (trialData.task_2 !== null && trialData.task_2 !== undefined && trialData.task_2);
    
    // Update timeline legend
    updateTimelineLegend(isDualTask);
    
    // Draw Channel 1 components (always active)
    if (trialData.dur_1 > 0) {
        drawComponent(
            trialData.start_1,
            trialData.start_1 + trialData.dur_1,
            yPositions.t1_cue,
            TIMELINE_COLORS.cue,
            `${trialData.task_1.toUpperCase()} Cue`
        );
    }
    
    // Draw Channel 1 stimulus pathways based on what's active
    if (trialData.dur_mov_1 > 0) {
        drawComponent(
            trialData.start_mov_1,
            trialData.start_mov_1 + trialData.dur_mov_1,
            yPositions.t1_stim,
            trialData.task_1 === 'mov' ? TIMELINE_COLORS.stimPrimary : TIMELINE_COLORS.stimDistractor,
            `${trialData.task_1 === 'mov' ? 'Primary' : 'Distractor'} Movement`
        );
    }
    
    if (trialData.dur_or_1 > 0) {
        drawComponent(
            trialData.start_or_1,
            trialData.start_or_1 + trialData.dur_or_1,
            yPositions.t2_stim,
            trialData.task_1 === 'or' ? TIMELINE_COLORS.stimPrimary : TIMELINE_COLORS.stimDistractor,
            `${trialData.task_1 === 'or' ? 'Primary' : 'Distractor'} Orientation`
        );
    }
    
    // Draw Channel 2 components (only if dual-task)
    if (isDualTask) {
        if (trialData.dur_2 > 0) {
            drawComponent(
                trialData.start_2,
                trialData.start_2 + trialData.dur_2,
                yPositions.t2_cue,
                TIMELINE_COLORS.go,
                `${trialData.task_2.toUpperCase()} Cue`
            );
        }
        
        // Draw Channel 2 stimulus pathways based on what's active
        if (trialData.dur_mov_2 > 0) {
            drawComponent(
                trialData.start_mov_2,
                trialData.start_mov_2 + trialData.dur_mov_2,
                yPositions.t1_stim, // Use different y-position if needed
                TIMELINE_COLORS.stimPrimary,
                "T2 Movement"
            );
        }
        
        if (trialData.dur_or_2 > 0) {
            drawComponent(
                trialData.start_or_2,
                trialData.start_or_2 + trialData.dur_or_2,
                yPositions.t2_stim,
                TIMELINE_COLORS.stimPrimary,
                "T2 Orientation"
            );
        }
        
        // Calculate SOA for dual-task (between the two primary stimuli)
        let t1_stim_start = trialData.task_1 === 'mov' ? trialData.start_mov_1 : trialData.start_or_1;
        let t2_stim_start = trialData.task_2 === 'mov' ? trialData.start_mov_2 : trialData.start_or_2;
        
        if (t1_stim_start && t2_stim_start) {
            const soa = t2_stim_start - t1_stim_start;
            const soaLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
            soaLabel.setAttribute("x", width - 10);
            soaLabel.setAttribute("y", 20);
            soaLabel.setAttribute("text-anchor", "end");
            soaLabel.setAttribute("fill", "#333");
            soaLabel.setAttribute("font-size", "12px");
            soaLabel.setAttribute("font-weight", "bold");
            soaLabel.textContent = `SOA: ${soa}ms`;
            barsGroup.appendChild(soaLabel);
        }
    } else if (trialData.dur_or_1 > 0 && trialData.dur_mov_1 > 0) {
        // Single-task with distractor - calculate SOA between target and distractor
        const soa = trialData.start_or_1 - trialData.start_mov_1;
        const soaLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
        soaLabel.setAttribute("x", width - 10);
        soaLabel.setAttribute("y", 20);
        soaLabel.setAttribute("text-anchor", "end");
        soaLabel.setAttribute("fill", "#333");
        soaLabel.setAttribute("font-size", "12px");
        soaLabel.setAttribute("font-weight", "bold");
        soaLabel.textContent = `SOA: ${soa}ms`;
        g.appendChild(soaLabel);
    }
}

async function runSelectedExperiment() {
    const select = document.getElementById('experiment-select');
    const startButton = document.getElementById('start-experiment');
    
    // Disable button to prevent multiple clicks
    if (startButton) {
        startButton.disabled = true;
        startButton.textContent = 'Running...';
    }
    
    select.blur(); // remove focus from the dropdown
    const selectedBlockId = select.value;
    
    if (!selectedBlockId) {
        if (startButton) {
            startButton.disabled = false;
            startButton.textContent = 'Start Experiment';
        }
        return;
    }

    // Get the block data
    const blocks = groupByBlock(resolvedData);
    const blockConditions = blocks[selectedBlockId];
    
    if (!blockConditions || blockConditions.length === 0) {
        console.error('No conditions found for block:', selectedBlockId);
        const canvasContainer = document.getElementById('canvas-container');
        canvasContainer.innerHTML = '<div class="error">No conditions found for selected experiment</div>';
        if (startButton) {
            startButton.disabled = false;
            startButton.textContent = 'Start Experiment';
        }
        return;
    }

    // Use the primary condition for trial generation (future enhancement: use full block)
    const condition = blockConditions[0];

    // Use the pre-generated trial sequence that was created when experiment was selected
    const trialSequence = currentTrialSequence.length > 0 ? currentTrialSequence : createTrialSequence(condition, 10);
    
    console.log('Running experiment with trial sequence:', trialSequence);
    
    // Clear canvas container and run experiment sequence
    const canvasContainer = document.getElementById('canvas-container');
    canvasContainer.focus()
    
    // Run the super experiment sequence
    try {
        // Set key mappings based on response set relationship
        const responseSetRelationship = condition.Simplified_RSO || 'Identical';
        const keyMappings = {
            Identical: {
                movementKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' },
                orientationKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' }
            },
            Disjoint: {
                movementKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' },
                orientationKeyMap: { 180: 'j', 0: 'l', 90: 'i', 270: 'k' }
            }
        };
        
        const mappingKey = responseSetRelationship.includes('Identical') ? 'Identical' : 'Disjoint';
        const config = {
            movementKeyMap: keyMappings[mappingKey].movementKeyMap,
            orientationKeyMap: keyMappings[mappingKey].orientationKeyMap
        };
        
        // Run trial sequence
        for (let i = 0; i < trialSequence.length; i++) {
            const trial = trialSequence[i];
            
            // Update display for current trial
            const trialStatus = document.getElementById('trial-status');
            if (trialStatus) {
                trialStatus.textContent = `Running trial ${trial.trialNumber}/${trialSequence.length} (${trial.taskType})`;
                trialStatus.style.display = 'block';
            }
            
            // Update timeline to show current trial's timing
            drawTimeline(trial.seParams);
            
            // Clean up previous trial
            await superExperiment.endBlock();
            
            // Add a brief pause between trials to show progress
            await new Promise(resolve => setTimeout(resolve, 100));
            
            // Run trial with its specific regen time
            const data = await superExperiment.block([trial.seParams], trial.regenTime, config, false, true, null, canvasContainer);
            console.log(`Trial ${trial.trialNumber} completed. Data:`, data);
        }
        
        console.log('Full experiment sequence completed');
        canvasContainer.innerHTML = '<div style="color: green; padding: 20px;">Experiment sequence completed successfully!</div>';
        
        // Hide trial status and show completion message there instead
        const trialStatus = document.getElementById('trial-status');
        if (trialStatus) {
            trialStatus.textContent = 'Experiment completed successfully!';
            trialStatus.style.display = 'block';
        }
        
    } catch (error) {
        console.error('Error running experiment sequence:', error);
        console.error('Error stack:', error.stack);
        canvasContainer.innerHTML = '<div style="color: red; padding: 20px;">Error running experiment sequence. Check console for details.</div>';
        
        // Clean up on error
        try {
            await superExperiment.endBlock();
        } catch (cleanupError) {
            console.error('Error during cleanup:', cleanupError);
        }
    } finally {
        // Re-enable the start button
        if (startButton) {
            startButton.disabled = false;
            startButton.textContent = 'Start Experiment';
        }
    }
}
 
// Main dropdown event handler
function updateUIForSelection() {
    const select = document.getElementById('experiment-select');
    const selectedBlockId = select.value;
    const startButton = document.getElementById('start-experiment');
    
    if (!selectedBlockId) {
        // Reset to initial state
        currentTrialSequence = []; // Clear pre-generated sequence
        document.getElementById('canvas-container').innerHTML = '<div class="placeholder">Select an experiment to begin</div>';
        document.getElementById('info-panel').innerHTML = '<div class="placeholder">Experiment details will appear here</div>';
        setSvgMessage(document.getElementById('timeline-svg'), 'Timeline will appear here');
        
        // Hide trial status
        const trialStatus = document.getElementById('trial-status');
        if (trialStatus) trialStatus.style.display = 'none';
        
        if (startButton) startButton.disabled = true;
        return;
    }
    
    // Enable start button when experiment is selected
    if (startButton) startButton.disabled = false;
    
    try {
        // Get the block data
        const blocks = groupByBlock(resolvedData);
        const blockConditions = blocks[selectedBlockId];
        
        if (!blockConditions || blockConditions.length === 0) {
            console.error('No conditions found for block:', selectedBlockId);
            document.getElementById('canvas-container').innerHTML = '<div class="error">No conditions found for selected experiment</div>';
            document.getElementById('info-panel').innerHTML = '<div class="error">Experiment data not found</div>';
            setSvgMessage(document.getElementById('timeline-svg'), 'Error: No data found', 'error');
            return;
        }
        
        // Use the first condition in the block for display purposes
        const primaryCondition = blockConditions[0];
        const conceptualRow = conceptualData.find(row => row.Experiment === primaryCondition.Experiment);
        
        // Update info panel
        if (conceptualRow) {
            updateInfoPanel(conceptualRow);
        } else {
            // Fallback info panel with condition data
            updateInfoPanelFromCondition(primaryCondition);
        }
        
        // Generate full trial sequence - this will be used for both preview and actual experiment
        try {
            // Generate the actual trial sequence that will be used when experiment runs
            currentTrialSequence = createTrialSequence(primaryCondition, 10); // Generate 10 trials
            
            if (currentTrialSequence.length > 0) {
                // Draw timeline using the FIRST trial that will actually run
                drawTimeline(currentTrialSequence[0].seParams);
                
                // Update info panel to show the distribution info (not specific sampled values)
                if (conceptualRow) {
                    updateInfoPanel(conceptualRow);
                } else {
                    updateInfoPanelFromCondition(primaryCondition);
                }
            } else {
                throw new Error('No trials generated');
            }
        } catch (timelineError) {
            console.error('Error generating sample trial for timeline:', timelineError);
            // Fall back to showing error
            setSvgMessage(document.getElementById('timeline-svg'), 'Error generating timeline', 'error');
        }
        
        // Clear canvas container - experiment is ready
        document.getElementById('canvas-container').innerHTML = '';
        
    } catch (error) {
        console.error('Error in updateUIForSelection:', error);
        document.getElementById('canvas-container').innerHTML = '<div class="error">Error loading experiment data</div>';
        document.getElementById('info-panel').innerHTML = '<div class="error">Error loading experiment information</div>';
        setSvgMessage(document.getElementById('timeline-svg'), 'Error loading timeline', 'error');
    }
}

// Fallback info panel update when conceptual data is not available
function updateInfoPanelFromCondition(condition) {
    const infoPanel = document.getElementById('info-panel');
    
    if (!condition) {
        infoPanel.innerHTML = '<div class="error">Condition data not found</div>';
        return;
    }
    
    // Helper function to safely get values
    const getValue = (value) => (value && value !== 'undefined' && value.trim() !== '') ? value : 'N/A';
    
    const numTasks = parseInt(condition.N_Tasks, 10) || 1;
    
    
    // Check for SOA distribution in condition's mapping notes  
    let soaDisplayValue = 'N/A';
    try {
        const mappingNotes = extractMappingNotes(condition);
        const viewerConfig = mappingNotes.viewer_config || {};
        
        if (viewerConfig.SOA_distribution === 'choice' && viewerConfig.SOA_values) {
            soaDisplayValue = `Choice from [${viewerConfig.SOA_values.join(', ')}]ms`;
        } else if (viewerConfig.SOA_distribution === 'uniform' && viewerConfig.SOA_range) {
            soaDisplayValue = `Uniform(${viewerConfig.SOA_range[0]}, ${viewerConfig.SOA_range[1]})ms`;
        } else {
            // Fallback to static SOA value (only SOA-related columns)
            const staticSOA = getValue(condition['Inter-task SOA']) || getValue(condition.SOA);
            soaDisplayValue = staticSOA !== 'N/A' ? `${staticSOA}ms` : 'N/A';
        }
    } catch (e) {
        // If extractMappingNotes fails, fallback to static SOA value
        const staticSOA = getValue(condition['Inter-task SOA']) || getValue(condition.SOA);
        soaDisplayValue = staticSOA !== 'N/A' ? `${staticSOA}ms` : 'N/A';
    }
    
    // Clear and rebuild info panel using DOM construction
    infoPanel.innerHTML = '';
    
    // Create header
    const header = document.createElement('h3');
    header.textContent = 'Experiment Details';
    infoPanel.appendChild(header);
    
    // Create definition list for organized layout
    const dl = document.createElement('dl');
    
    // Add experiment info rows
    addInfoRow(dl, 'Experiment', getValue(condition.Experiment));
    addInfoRow(dl, 'Number of Tasks', numTasks.toString());
    addInfoRow(dl, 'SOA', soaDisplayValue);
    addInfoRow(dl, 'Task 1 Type', getValue(condition.Task_1_Type));
    
    if (numTasks > 1) {
        addInfoRow(dl, 'Task 2 Type', getValue(condition.Task_2_Type));
    }
    
    addInfoRow(dl, 'Stimulus Valency', getValue(condition.Stimulus_Valency));
    addInfoRow(dl, 'Response Set Overlap', getValue(condition.Simplified_RSO));
    
    // Add SRM info based on number of tasks
    if (numTasks === 1) {
        addInfoRow(dl, 'Stimulus Response Mapping', getValue(condition.SRM_1));
    } else {
        addInfoRow(dl, 'Task 1 SRM', getValue(condition.SRM_1));
        addInfoRow(dl, 'Task 2 SRM', getValue(condition.SRM_2));
    }
    
    addInfoRow(dl, 'Sequence Type', getValue(condition.Sequence_Type));
    const switchRate = getValue(condition.Switch_Rate_Percent);
    addInfoRow(dl, 'Switch Rate', switchRate !== 'N/A' && condition.Switch_Rate_Percent ? `${switchRate}%` : switchRate);
    
    const itiValue = getValue(condition.ITI_ms);
    const itiType = getValue(condition.RSI_Distribution_Type || condition.ITI_Distribution_Type);
    const itiDisplay = itiValue !== 'N/A' && condition.ITI_ms ? `${itiValue}ms (${itiType})` : `${itiValue} (${itiType})`;
    addInfoRow(dl, 'ITI', itiDisplay);
    
    infoPanel.appendChild(dl);
}

// Helper function to set SVG message
function setSvgMessage(svg, text, className = 'placeholder') {
    const color = className === 'error' ? 'var(--danger)' : 'var(--muted)';
    svg.innerHTML = `<text x="50%" y="50%" text-anchor="middle" fill="${color}" font-style="italic">${text}</text>`;
}

// Show loading state with skeletons
function showLoadingState() {
    const canvasContainer = document.getElementById('canvas-container');
    const infoPanel = document.getElementById('info-panel');
    const timelineSvg = document.getElementById('timeline-svg');
    const legend = document.getElementById('timeline-legend');
    
    // Canvas skeleton
    canvasContainer.innerHTML = '<div class="skeleton skeleton-canvas"></div>';
    
    // Info panel skeleton
    infoPanel.innerHTML = '<div class="skeleton skeleton-info"></div>';
    
    // Timeline skeleton
    setSvgMessage(timelineSvg, 'Loading...', 'loading');
    
    // Hide legend
    if (legend) legend.style.display = 'none';
}

// Show error state
function showErrorState(message) {
    const canvasContainer = document.getElementById('canvas-container');
    const infoPanel = document.getElementById('info-panel');
    const timelineSvg = document.getElementById('timeline-svg');
    const legend = document.getElementById('timeline-legend');
    
    canvasContainer.innerHTML = `<div class="error">${message}</div>`;
    infoPanel.innerHTML = '<div class="error">Error loading experiment data</div>';
    setSvgMessage(timelineSvg, 'Error loading data', 'error');
    
    // Hide legend
    if (legend) legend.style.display = 'none';
}

// Initialize the application
async function initializeApp() {
    try {
        showLoadingState();
        
        // Load both CSV files with better error handling
        console.log('Loading CSV files...');
        
        const [resolvedResponse, conceptualResponse] = await Promise.all([
            fetch('data/resolved_design_space.csv').catch(e => { throw new Error(`Failed to load resolved data: ${e.message}`); }),
            fetch('data/super_experiment_design_space.csv').catch(e => { throw new Error(`Failed to load conceptual data: ${e.message}`); })
        ]);
        
        if (!resolvedResponse.ok) {
            throw new Error(`Failed to load resolved data: ${resolvedResponse.status} ${resolvedResponse.statusText}`);
        }
        if (!conceptualResponse.ok) {
            throw new Error(`Failed to load conceptual data: ${conceptualResponse.status} ${conceptualResponse.statusText}`);
        }
        
        const resolvedText = await resolvedResponse.text();
        const conceptualText = await conceptualResponse.text();
        
        // Parse CSV data with error handling
        try {
            resolvedData = parseCSV(resolvedText);
            conceptualData = parseCSV(conceptualText);
        } catch (parseError) {
            throw new Error(`Failed to parse CSV data: ${parseError.message}`);
        }
        
        console.log(`Loaded ${resolvedData.length} resolved experiments`);
        console.log(`Loaded ${conceptualData.length} conceptual experiments`);
        
        // Validate and filter data
        const initialResolvedCount = resolvedData.length;
        resolvedData = resolvedData.filter(row => row.Experiment && row.Experiment.trim() !== '');
        
        if (resolvedData.length === 0) {
            throw new Error('No valid experiments found in the data files');
        }
        
        console.log(`Using ${resolvedData.length} total experiments (filtered from ${initialResolvedCount})`);
        
        // Group data by Block_ID for block-aware functionality
        const blocks = groupByBlock(resolvedData);
        const blockKeys = Object.keys(blocks);
        
        if (blockKeys.length === 0) {
            throw new Error('No experiment blocks found');
        }
        
        console.log(`Grouped into ${blockKeys.length} blocks`);
        
        // Populate dropdown with blocks
        const select = document.getElementById('experiment-select');
        
        // Clear existing options except the placeholder
        const placeholder = select.querySelector('option[value=""]');
        select.innerHTML = '';
        if (placeholder) select.appendChild(placeholder);
        
        // Sort blocks alphabetically for better UX
        blockKeys.sort().forEach(blockId => {
            const option = document.createElement('option');
            option.value = blockId;
            option.textContent = blockId;
            select.appendChild(option);
        });
        
        // Add event listeners
        select.addEventListener('change', updateUIForSelection);
        const startButton = document.getElementById('start-experiment');
        if (startButton) {
            startButton.addEventListener('click', runSelectedExperiment);
        }
        
        // Reset to initial state
        updateUIForSelection();
        
        console.log('App initialized successfully');
        
    } catch (error) {
        console.error('Error initializing app:', error);
        showErrorState(`Error loading experiment data: ${error.message}`);
    }
}

// Start the app when page loads (only in browser environment)
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', initializeApp);
}

// Export for Node.js environment (for testing)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        parseCSV,
        convertAbsoluteToSEParams,
        generateTrialDirections,
        generateITI,
        generateSOA,
        generateDynamicSOA,
        recalculateTimingsWithDynamicSOA,
        extractMappingNotes,
        groupByBlock,
        extractViewerConfig,
        getTrialTransitionType,
        generateTaskSequence,
        generateTaskAssignmentSequence,
        createTrialSequence,
        updateInfoPanel,
        updateInfoPanelFromCondition,
        drawTimeline,
        showLoadingState,
        showErrorState
    };
}

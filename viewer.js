// Global variables to store experiment data
let resolvedData = [];
let conceptualData = [];

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
        
        // Channel 1 (movement task): Primary movement stimulus
        seParams.start_mov_1 = mov_start;
        seParams.dur_mov_1 = mov_duration;
        
        // Channel 2 (orientation task): Primary orientation stimulus  
        seParams.start_or_2 = or_start;
        seParams.dur_or_2 = or_duration;
        
        // For dual-task, check if we need distractors (bivalent stimuli)
        // This is a simplified approach - in reality, you'd check stimulus valency per channel
        // For now, assume univalent stimuli in dual-task (no cross-channel distractors)
        seParams.start_or_1 = 0;
        seParams.dur_or_1 = 0;
        seParams.start_mov_2 = 0;
        seParams.dur_mov_2 = 0;
        
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
    seParams.stimulusCongruency = 'neutral';
    
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

// Generate ITI for a trial based on distribution parameters
function generateITI(condition) {
    const distributionType = condition.ITI_Distribution_Type || 'fixed';
    const baseITI = parseFloat(condition.ITI_ms) || 1000;
    
    if (distributionType === 'fixed') {
        return baseITI;
    }
    
    // Parse distribution parameters
    let params = [];
    try {
        if (condition.ITI_Distribution_Params && condition.ITI_Distribution_Params !== '[]') {
            params = JSON.parse(condition.ITI_Distribution_Params);
        }
    } catch (e) {
        console.warn('Failed to parse ITI_Distribution_Params:', condition.ITI_Distribution_Params);
        return baseITI;
    }
    
    if (distributionType === 'uniform' && params.length >= 2) {
        // Uniform distribution between min and max
        const [min, max] = params;
        return min + Math.random() * (max - min);
    } else if (distributionType === 'choice' && params.length > 0) {
        // Random choice from array of values
        return params[Math.floor(Math.random() * params.length)];
    }
    
    // Default to base ITI if distribution can't be processed
    return baseITI;
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

// Advanced trial sequence generation
function createTrialSequence(condition, numTrials = 10) {
    const trialSequence = [];
    
    // Parse sequence parameters
    const sequenceType = condition.Sequence_Type || 'Random';
    const switchRate = parseFloat(condition.Switch_Rate_Percent) || 0;
    
    // Determine paradigm type from N_Tasks (new approach)
    const nTasks = condition.N_Tasks || 1;
    const isDualTask = (nTasks == 2);
    
    // Generate assignment sequence based on paradigm type
    let assignmentSequence;
    
    if (isDualTask) {
        // DUAL-TASK: Generate task-to-channel assignments using switch rate
        // Default mapping: Task 1 -> 'mov', Task 2 -> 'or'
        assignmentSequence = generateTaskAssignmentSequence(
            'mov',  // Always map Task 1 to movement
            'or',   // Always map Task 2 to orientation 
            numTrials, 
            switchRate
        );
    } else {
        // SINGLE-TASK: Generate task sequence using switch rate
        const taskSequence = generateTaskSequence(sequenceType, numTrials, switchRate);
        // Convert to assignment format for consistency
        assignmentSequence = taskSequence.map(task => ({ currentTask: task }));
    }
    
    // Generate trials
    for (let i = 0; i < numTrials; i++) {
        const assignment = assignmentSequence[i];
        const directions = generateTrialDirections(condition, assignment);
        const iti = generateITI(condition);
        
        // Get base parameters from CSV data
        const baseParams = convertAbsoluteToSEParams(condition);
        
        let trialParams;
        
        if (isDualTask) {
            // DUAL-TASK: Both channels active, task assignment may vary per trial
            trialParams = {
                ...baseParams,
                task_1: assignment.channel1_task,  // Dynamic assignment based on switch rate
                task_2: assignment.channel2_task,  // Dynamic assignment based on switch rate
                
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
                task_1: assignment.currentTask,  // Dynamic task assignment for task-switching
                task_2: null,                    // Channel 2 always inactive for single-task
                
                // Apply generated directions (only Channel 1 pathways will have non-null values)
                dir_mov_1: directions.dir_mov_1 || 0,
                dir_or_1: directions.dir_or_1 || 0,
                dir_mov_2: 0,  // Channel 2 always inactive
                dir_or_2: 0,   // Channel 2 always inactive
                
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
            regenTime: iti,
            trialNumber: i + 1,
            taskType: isDualTask ? `${assignment.channel1_task}+${assignment.channel2_task}` : assignment.currentTask
        });
    }
    
    return trialSequence;
}

// Update info panel with experiment details
function updateInfoPanel(conceptualRow) {
    const infoPanel = document.getElementById('info-panel');
    
    const info = `
        <h3>Experiment Details</h3>
        <p><strong>Experiment:</strong> ${conceptualRow.Experiment}</p>
        <p><strong>Number of Tasks:</strong> ${conceptualRow['Number of Tasks']}</p>
        <p><strong>SOA:</strong> ${conceptualRow.SOA}ms</p>
        <p><strong>Task 1 Type:</strong> ${conceptualRow['Task 1 Type']}</p>
        <p><strong>Task 2 Type:</strong> ${conceptualRow['Task 2 Type']}</p>
        <p><strong>Stimulus Valency:</strong> ${conceptualRow['Stimulus Valency']}</p>
        <p><strong>Response Set Overlap:</strong> ${conceptualRow['Response Set Overlap']}</p>
        <p><strong>Stimulus Response Mapping:</strong> ${conceptualRow['Stimulus Response Mapping']}</p>
        <p><strong>Notes:</strong> ${conceptualRow.Notes || 'N/A'}</p>
    `;
    
    infoPanel.innerHTML = info;
}

// Draw timeline visualization from trial-specific data
function drawTimeline(trialData) {
    const svg = document.getElementById('timeline-svg');
    
    // Optimization: Check if we need to redraw (compare with previous trial data)
    const trialKey = JSON.stringify({
        task_1: trialData.task_1,
        task_2: trialData.task_2,
        start_1: trialData.start_1,
        dur_1: trialData.dur_1,
        start_2: trialData.start_2,
        dur_2: trialData.dur_2,
        start_mov_1: trialData.start_mov_1,
        dur_mov_1: trialData.dur_mov_1,
        start_or_1: trialData.start_or_1,
        dur_or_1: trialData.dur_or_1,
        start_mov_2: trialData.start_mov_2,
        dur_mov_2: trialData.dur_mov_2,
        start_or_2: trialData.start_or_2,
        dur_or_2: trialData.dur_or_2,
        regenTime: trialData.regenTime || 0
    });
    
    // Skip redraw if timeline structure is identical
    if (svg.getAttribute('data-trial-key') === trialKey) {
        return;
    }
    svg.setAttribute('data-trial-key', trialKey);
    
    // Clear previous timeline
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
    
    // Create main group
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `translate(${margin.left},${margin.top})`);
    svg.appendChild(g);
    
    // Draw time axis
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", "0");
    axis.setAttribute("y1", height);
    axis.setAttribute("x2", width);
    axis.setAttribute("y2", height);
    axis.setAttribute("stroke", "#333");
    axis.setAttribute("stroke-width", "2");
    g.appendChild(axis);
    
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
        tick.setAttribute("stroke", "#333");
        tick.setAttribute("stroke-width", "1");
        g.appendChild(tick);
        
        // Label
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", x);
        label.setAttribute("y", height + 20);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", "#333");
        label.setAttribute("font-size", "10px");
        label.textContent = `${t}ms`;
        g.appendChild(label);
    }
    
    // Define y-positions for the timeline elements
    const yPositions = {
        t1_cue: 30,
        t1_stim: 60,
        t2_cue: 120,
        t2_stim: 150
    };
    
    // Draw axis labels
    function drawAxisLabel(label, yPos) {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", -10);
        text.setAttribute("y", yPos + 15);
        text.setAttribute("text-anchor", "end");
        text.setAttribute("fill", "#333");
        text.setAttribute("font-size", "12px");
        text.setAttribute("font-weight", "bold");
        text.textContent = label;
        g.appendChild(text);
    }
    
    drawAxisLabel("T1 Cue", yPositions.t1_cue);
    drawAxisLabel("T1 Stimulus", yPositions.t1_stim);
    drawAxisLabel("T2 Cue", yPositions.t2_cue);
    drawAxisLabel("T2 Stimulus", yPositions.t2_stim);
    
    // Draw timeline components
    function drawComponent(startTime, endTime, yPos, color, label) {
        if (startTime >= endTime) return;
        
        const x = startTime * width / timelineEnd;
        const componentWidth = Math.max(2, (endTime - startTime) * width / timelineEnd);
        
        // Draw rectangle
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", yPos);
        rect.setAttribute("width", componentWidth);
        rect.setAttribute("height", "25");
        rect.setAttribute("fill", color);
        rect.setAttribute("opacity", "0.7");
        g.appendChild(rect);
        
        // Add timing labels if component is wide enough
        if (componentWidth > 40) {
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", x + componentWidth/2);
            text.setAttribute("y", yPos + 17);
            text.setAttribute("text-anchor", "middle");
            text.setAttribute("fill", "white");
            text.setAttribute("font-size", "9px");
            text.setAttribute("font-weight", "bold");
            text.textContent = `${startTime}-${endTime}ms`;
            g.appendChild(text);
        }
    }
    
    // Determine what to draw based on actual trial structure
    const isDualTask = (trialData.task_2 !== null);
    
    // Draw Channel 1 components (always active)
    if (trialData.dur_1 > 0) {
        drawComponent(
            trialData.start_1,
            trialData.start_1 + trialData.dur_1,
            yPositions.t1_cue,
            "#4CAF50",
            `${trialData.task_1.toUpperCase()} Cue`
        );
    }
    
    // Draw Channel 1 stimulus pathways based on what's active
    if (trialData.dur_mov_1 > 0) {
        drawComponent(
            trialData.start_mov_1,
            trialData.start_mov_1 + trialData.dur_mov_1,
            yPositions.t1_stim,
            trialData.task_1 === 'mov' ? "#2196F3" : "#90CAF9", // Darker if primary, lighter if distractor
            `${trialData.task_1 === 'mov' ? 'Primary' : 'Distractor'} Movement`
        );
    }
    
    if (trialData.dur_or_1 > 0) {
        drawComponent(
            trialData.start_or_1,
            trialData.start_or_1 + trialData.dur_or_1,
            yPositions.t2_stim,
            trialData.task_1 === 'or' ? "#2196F3" : "#90CAF9", // Darker if primary, lighter if distractor
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
                "#FF9800",
                `${trialData.task_2.toUpperCase()} Cue`
            );
        }
        
        // Draw Channel 2 stimulus pathways based on what's active
        if (trialData.dur_mov_2 > 0) {
            drawComponent(
                trialData.start_mov_2,
                trialData.start_mov_2 + trialData.dur_mov_2,
                yPositions.t1_stim, // Use different y-position if needed
                "#F44336",
                "T2 Movement"
            );
        }
        
        if (trialData.dur_or_2 > 0) {
            drawComponent(
                trialData.start_or_2,
                trialData.start_or_2 + trialData.dur_or_2,
                yPositions.t2_stim,
                "#F44336",
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
            g.appendChild(soaLabel);
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
    select.blur() // remove focus from the dropdown
    const selectedIndex = parseInt(select.value);

    const condition = resolvedData[selectedIndex]

    // Generate trial sequence
    const trialSequence = createTrialSequence(condition, 10);
    
    console.log('Running experiment with trial sequence:', trialSequence);
    
    // Clear canvas container and run experiment sequence
    const canvasContainer = document.getElementById('canvas-container');
    canvasContainer.focus()
    canvasContainer.innerHTML = '<div>Starting experiment sequence...</div>';
    
    // Run the super experiment sequence
    try {
        // Set key mappings based on response set relationship
        const responseSetRelationship = condition.Simplified_RSO || 'Identical';
        const keyMappings = {
            'Identical': {
                movementKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' },
                orientationKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' }
            },
            'Disjoint': {
                movementKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' },
                orientationKeyMap: { 90: 'w', 270: 's', 180: 'a', 0: 'd' }
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
            canvasContainer.innerHTML = `<div>Running trial ${trial.trialNumber}/${trialSequence.length} (${trial.taskType})</div>`;
            
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
    }
}
 
// Main dropdown event handler
function updateUIForSelection() {
    const select = document.getElementById('experiment-select');
    const selectedIndex = parseInt(select.value);
    
    if (isNaN(selectedIndex)) {
        // Reset to initial state
        document.getElementById('canvas-container').innerHTML = '<div class="placeholder">Select an experiment to begin</div>';
        document.getElementById('info-panel').innerHTML = '<div class="placeholder">Experiment details will appear here</div>';
        document.getElementById('timeline-svg').innerHTML = '<text x="50%" y="50%" text-anchor="middle" fill="#666" font-style="italic">Timeline will appear here</text>';
        return;
    }
    
    const condition = resolvedData[selectedIndex];
    const conceptualRow = conceptualData.find(row => row.Experiment === condition.Experiment);
    
    // Update info panel
    if (conceptualRow) {
        updateInfoPanel(conceptualRow);
    } else {
        // Fallback info panel with condition data
        updateInfoPanelFromCondition(condition);
    }
    
    // Generate a sample trial to visualize
    try {
        const sampleTrials = createTrialSequence(condition, 1);
        if (sampleTrials.length > 0) {
            // Draw timeline using actual trial data
            drawTimeline(sampleTrials[0].seParams);
        }
    } catch (error) {
        console.error('Error generating sample trial for timeline:', error);
        // Fall back to showing placeholder
        document.getElementById('timeline-svg').innerHTML = '<text x="50%" y="50%" text-anchor="middle" fill="#666" font-style="italic">Error generating timeline</text>';
    }
    
}

// Fallback info panel update when conceptual data is not available
function updateInfoPanelFromCondition(condition) {
    const infoPanel = document.getElementById('info-panel');
    
    const info = `
        <h3>Experiment Details</h3>
        <p><strong>Experiment:</strong> ${condition.Experiment}</p>
        <p><strong>Task 1 Type:</strong> ${condition.Task_1_Type || 'N/A'}</p>
        <p><strong>Task 2 Type:</strong> ${condition.Task_2_Type || 'N/A'}</p>
        <p><strong>Stimulus Valency:</strong> ${condition.Stimulus_Valency || 'N/A'}</p>
        <p><strong>Response Set Overlap:</strong> ${condition.Simplified_RSO || 'N/A'}</p>
        <p><strong>Sequence Type:</strong> ${condition.Sequence_Type || 'N/A'}</p>
        <p><strong>Switch Rate:</strong> ${condition.Switch_Rate_Percent || 0}%</p>
        <p><strong>ITI:</strong> ${condition.ITI_ms || 'N/A'}ms (${condition.ITI_Distribution_Type || 'fixed'})</p>
    `;
    
    infoPanel.innerHTML = info;
}

// Initialize the application
async function initializeApp() {
    try {
        // Load both CSV files
        console.log('Loading CSV files...');
        
        const [resolvedResponse, conceptualResponse] = await Promise.all([
            fetch('data/resolved_design_space.csv'),
            fetch('data/super_experiment_design_space.csv')
        ]);
        
        const resolvedText = await resolvedResponse.text();
        const conceptualText = await conceptualResponse.text();
        
        // Parse CSV data
        resolvedData = parseCSV(resolvedText);
        conceptualData = parseCSV(conceptualText);
        
        console.log(`Loaded ${resolvedData.length} resolved experiments`);
        console.log(`Loaded ${conceptualData.length} conceptual experiments`);
        
        // Use all data from the CSV without filtering
        resolvedData = resolvedData.filter(row => row.Experiment && row.Experiment.trim() !== '');
        
        console.log(`Using ${resolvedData.length} total experiments`);
        
        // Populate dropdown
        const select = document.getElementById('experiment-select');
        resolvedData.forEach((row, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = row.Experiment;
            select.appendChild(option);
        });
        
        // Add event listener
        select.addEventListener('change', updateUIForSelection);
	const startButton = document.getElementById('start-experiment');
	startButton.addEventListener('click', runSelectedExperiment)
        
        console.log('App initialized successfully');
        
    } catch (error) {
        console.error('Error initializing app:', error);
        document.getElementById('canvas-container').innerHTML = '<div style="color: red; padding: 20px;">Error loading experiment data. Check console for details.</div>';
    }
}

// Start the app when page loads
document.addEventListener('DOMContentLoaded', initializeApp);

module.exports = {
    parseCSV,
    convertAbsoluteToSEParams,
    generateTrialDirections,
    generateITI,
    generateTaskSequence,
    generateTaskAssignmentSequence,
    createTrialSequence,
    updateInfoPanel,
    drawTimeline
    // Add any other functions you want to test
};

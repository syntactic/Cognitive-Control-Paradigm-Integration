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
        // If stimulus is bivalent (like Stroop), both pathways of Channel 1 should be active
        // Check if both stimulus types have similar timing (indicating bivalent stimulus)
        const stimuliOverlap = Math.abs(mov_start - or_start) < 50 && Math.abs(mov_duration - or_duration) < 100;
        
        if (stimuliOverlap && or_duration > 0) {
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

// Generate trial directions based on condition metadata
function generateTrialDirections(condition) {
    // Parse stimulus valency and response set overlap to determine direction generation logic
    const stimulusValency = condition.Stimulus_Valency || 'Univalent';
    const responseSetOverlap = condition.Simplified_RSO || 'Identical';
    
    let mov_dir, or_dir;
    
    // For now, implement basic random direction generation
    // This can be enhanced based on specific valency and congruency rules
    if (stimulusValency.includes('Bivalent')) {
        if (stimulusValency.includes('Congruent')) {
            // Both stimuli should lead to same response
            mov_dir = Math.random() < 0.5 ? 0 : 180;
            or_dir = mov_dir; // Same direction for congruent
        } else if (stimulusValency.includes('Incongruent')) {
            // Stimuli should lead to opposite responses
            mov_dir = Math.random() < 0.5 ? 0 : 180;
            or_dir = mov_dir === 0 ? 180 : 0; // Opposite direction
        } else if (stimulusValency.includes('Neutral')) {
            // Neutral - stimuli should be orthogonal
            mov_dir = Math.random() < 0.5 ? 0 : 180; // left/right movement
            or_dir = Math.random() < 0.5 ? 90 : 270; // up/down orientation
        } else {
            // Plain "Bivalent" without specification - random directions
            mov_dir = Math.random() < 0.5 ? 0 : 180;
            or_dir = Math.random() < 0.5 ? 0 : 180;
        }
    } else {
        // Univalent - random directions since there's no crosstalk
        mov_dir = Math.random() < 0.5 ? 0 : 180;
        or_dir = Math.random() < 0.5 ? 0 : 180;
    }
    
    return { mov_dir, or_dir };
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

// Generate task sequence based on sequence type
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

// Advanced trial sequence generation
function createTrialSequence(condition, numTrials = 10) {
    const trialSequence = [];
    
    // Parse sequence parameters
    const sequenceType = condition.Sequence_Type || 'Random';
    const switchRate = parseFloat(condition.Switch_Rate_Percent) || 0;
    
    // Generate task sequence
    const taskSequence = generateTaskSequence(sequenceType, numTrials, switchRate);
    
    // Determine paradigm type from condition
    const cue2Duration = parseInt(condition.effective_end_cue2) - parseInt(condition.effective_start_cue2);
    const go2Duration = parseInt(condition.effective_end_go2) - parseInt(condition.effective_start_go2);
    const isDualTask = cue2Duration > 0 && go2Duration > 0;
    
    // Generate trials
    for (let i = 0; i < numTrials; i++) {
        const currentTask = taskSequence[i];
        const directions = generateTrialDirections(condition);
        const iti = generateITI(condition);
        
        let trialParams;
        
        if (isDualTask) {
            // DUAL-TASK PARADIGM: Use base parameters from convertAbsoluteToSEParams
            // Both channels are active with fixed task assignments
            const baseParams = convertAbsoluteToSEParams(condition);
            
            trialParams = {
                ...baseParams,
                // Override directions for active pathways
                dir_mov_1: baseParams.dur_mov_1 > 0 ? directions.mov_dir : 0,
                dir_or_1: baseParams.dur_or_1 > 0 ? directions.or_dir : 0,
                dir_mov_2: baseParams.dur_mov_2 > 0 ? directions.mov_dir : 0,
                dir_or_2: baseParams.dur_or_2 > 0 ? directions.or_dir : 0,
            };
            
        } else {
            // SINGLE-TASK/TASK-SWITCHING PARADIGM: Only Channel 1 active, task_1 varies
            // Create base parameters but modify for the current task
            const baseCondition = { ...condition };
            const baseParams = convertAbsoluteToSEParams(baseCondition);
            
            // Override task assignment and stimulus pathways based on current task
            trialParams = {
                ...baseParams,
                task_1: currentTask,  // Dynamic task assignment for task-switching
                task_2: null,         // Channel 2 always inactive for single-task
                
                // Channel 2 completely inactive
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
                dir_mov_2: 0,
                dir_or_2: 0,
            };
            
            // Configure Channel 1 stimulus pathways based on current task and stimulus valency
            if (currentTask === 'mov') {
                // Movement task: primary movement stimulus
                trialParams.dir_mov_1 = directions.mov_dir;
                trialParams.dir_or_1 = trialParams.dur_or_1 > 0 ? directions.or_dir : 0; // distractor if bivalent
            } else if (currentTask === 'or') {
                // Orientation task: reconfigure Channel 1 for orientation as primary task
                // Swap the pathways so orientation becomes primary
                const temp_start = trialParams.start_mov_1;
                const temp_dur = trialParams.dur_mov_1;
                const temp_coh = trialParams.coh_mov_1;
                
                trialParams.start_mov_1 = trialParams.start_or_1;
                trialParams.dur_mov_1 = trialParams.dur_or_1;
                trialParams.coh_mov_1 = trialParams.coh_or_1;
                trialParams.dir_mov_1 = directions.or_dir; // orientation direction goes to mov pathway
                
                trialParams.start_or_1 = temp_start;
                trialParams.dur_or_1 = temp_dur;
                trialParams.coh_or_1 = temp_coh;
                trialParams.dir_or_1 = temp_dur > 0 ? directions.mov_dir : 0; // movement as distractor if bivalent
            }
        }
        
        trialSequence.push({
            seParams: trialParams,
            regenTime: iti,
            trialNumber: i + 1,
            taskType: currentTask
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

// Draw timeline visualization
function drawTimeline(absoluteRow) {
    const svg = document.getElementById('timeline-svg');
    
    // Clear previous timeline
    svg.innerHTML = '';
    
    // Timeline settings
    const timelineStart = 0;
    const timelineEnd = Math.max(
        parseInt(absoluteRow.effective_end_stim1_or),
        parseInt(absoluteRow.effective_end_stim1_mov),
        parseInt(absoluteRow.effective_end_go2),
        parseInt(absoluteRow.effective_end_cue2)
    ) + 500; // Add padding
    
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
    
    // Draw T1 components (using cue1 and stim1_mov data)
    drawComponent(
        parseInt(absoluteRow.effective_start_cue1),
        parseInt(absoluteRow.effective_end_cue1),
        yPositions.t1_cue,
        "#4CAF50",
        "T1 Cue"
    );
    
    drawComponent(
        parseInt(absoluteRow.effective_start_stim1_mov),
        parseInt(absoluteRow.effective_end_stim1_mov),
        yPositions.t1_stim,
        "#2196F3",
        "T1 Stimulus"
    );
    
    // Draw T2 components (using cue2 and stim1_or data)
    drawComponent(
        parseInt(absoluteRow.effective_start_cue2),
        parseInt(absoluteRow.effective_end_cue2),
        yPositions.t2_cue,
        "#FF9800",
        "T2 Cue"
    );
    
    drawComponent(
        parseInt(absoluteRow.effective_start_stim1_or),
        parseInt(absoluteRow.effective_end_stim1_or),
        yPositions.t2_stim,
        "#F44336",
        "T2 Stimulus"
    );
    
    // Add SOA indicator
    const soa = parseInt(absoluteRow.effective_start_stim1_or) - parseInt(absoluteRow.effective_start_stim1_mov);
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
    
    // Draw timeline
    drawTimeline(condition);
    
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
    createTrialSequence,
    updateInfoPanel,
    drawTimeline
    // Add any other functions you want to test
};

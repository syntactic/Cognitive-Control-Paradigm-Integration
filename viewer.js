// Global variables to store experiment data
let resolvedData = [];
let conceptualData = [];

// Simple CSV parser
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        for (let j = 0; j < headers.length; j++) {
            row[headers[j]] = values[j];
        }
        data.push(row);
    }
    
    return data;
}

// Convert absolute timing data to super-experiment parameters
function convertAbsoluteToSEParams(absoluteRow) {
    const seParams = {};
    
    // Determine task types based on the conceptual data
    // For Telford experiments, T1 maps to mov pathway, T2 maps to or pathway
    seParams.task_1 = 'mov';  // T1 -> movement pathway
    seParams.task_2 = 'or';   // T2 -> orientation pathway
    
    // Convert absolute timings to relative timings for T1 (mov pathway)
    seParams.start_mov_1 = parseInt(absoluteRow.effective_start_stim1_mov);
    seParams.dur_mov_1 = parseInt(absoluteRow.effective_end_stim1_mov) - parseInt(absoluteRow.effective_start_stim1_mov);
    
    // T2 uses or pathway
    seParams.start_or_1 = parseInt(absoluteRow.effective_start_stim1_or);
    seParams.dur_or_1 = parseInt(absoluteRow.effective_end_stim1_or) - parseInt(absoluteRow.effective_start_stim1_or);
    
    // Set _2 pathway parameters to 0 since these are dual-task on separate pathways
    seParams.start_mov_2 = 0;
    seParams.dur_mov_2 = 0;
    seParams.start_or_2 = 0;
    seParams.dur_or_2 = 0;
    
    // Convert cue timings (task-agnostic: _1 and _2)
    seParams.start_1 = parseInt(absoluteRow.effective_start_cue1);
    seParams.dur_1 = parseInt(absoluteRow.effective_end_cue1) - parseInt(absoluteRow.effective_start_cue1);
    
    seParams.start_2 = parseInt(absoluteRow.effective_start_cue2);
    seParams.dur_2 = parseInt(absoluteRow.effective_end_cue2) - parseInt(absoluteRow.effective_start_cue2);
    
    // Convert go signal timings (task-agnostic: _go_1 and _go_2)
    seParams.start_go_1 = parseInt(absoluteRow.effective_start_go1);
    seParams.dur_go_1 = parseInt(absoluteRow.effective_end_go1) - parseInt(absoluteRow.effective_start_go1);
    
    seParams.start_go_2 = parseInt(absoluteRow.effective_start_go2);
    seParams.dur_go_2 = parseInt(absoluteRow.effective_end_go2) - parseInt(absoluteRow.effective_start_go2);
    
    // Set stimulus parameters
    seParams.coh_1 = parseFloat(absoluteRow.coh_1);
    seParams.coh_2 = parseFloat(absoluteRow.coh_2);
    
    // Set default directions (can be random for demo)
    seParams.dir_mov_1 = Math.random() < 0.5 ? 0 : 180;
    seParams.dir_or_1 = Math.random() < 0.5 ? 0 : 180;
    seParams.dir_mov_2 = 0;
    seParams.dir_or_2 = 0;
    
    // Set key mappings for identical response sets
    seParams.movementKeyMap = { 180: 'a', 0: 'd' };
    seParams.orientationKeyMap = { 180: 'a', 0: 'd' };
    
    // Set response set relationship and stimulus congruency
    seParams.responseSetRelationship = 'identical';
    seParams.stimulusCongruency = 'neutral';
    
    return seParams;
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

// Create a single trial from parameters (similar to createTrialSequence)
function createSingleTrial(params) {
    // Generate directions based on congruency settings
    const mov_dir = Math.random() < 0.5 ? 0 : 180;
    const or_dir = Math.random() < 0.5 ? 0 : 180;
    
    // Create trial with the paradigm's timing parameters
    // This is a dual-task paradigm, so both tasks are active
    const trial = {
        ...params,
        // Set directions and coherence for both tasks
        dir_mov_1: mov_dir,
        dir_or_1: or_dir,
        dir_mov_2: mov_dir,
        dir_or_2: or_dir,
        
        // Set coherence values
        coh_mov_1: params.coh_1,
        coh_or_1: params.coh_2,
        coh_mov_2: params.coh_1,
        coh_or_2: params.coh_2
    };
    
    return trial;
}

// Main dropdown event handler
async function onExperimentChange() {
    const select = document.getElementById('experiment-select');
    const selectedIndex = parseInt(select.value);
    
    if (isNaN(selectedIndex)) {
        // Reset to initial state
        document.getElementById('canvas-container').innerHTML = '<div class="placeholder">Select an experiment to begin</div>';
        document.getElementById('info-panel').innerHTML = '<div class="placeholder">Experiment details will appear here</div>';
        document.getElementById('timeline-svg').innerHTML = '<text x="50%" y="50%" text-anchor="middle" fill="#666" font-style="italic">Timeline will appear here</text>';
        return;
    }
    
    const absoluteRow = resolvedData[selectedIndex];
    const conceptualRow = conceptualData.find(row => row.Experiment === absoluteRow.Experiment);
    
    // Update info panel
    if (conceptualRow) {
        updateInfoPanel(conceptualRow);
    }
    
    // Draw timeline
    drawTimeline(absoluteRow);
    
    // Convert parameters and create trial
    const seParams = convertAbsoluteToSEParams(absoluteRow);
    const trial = createSingleTrial(seParams);
    
    console.log('Running experiment with parameters:', trial);
    
    // Clear canvas container and run experiment
    const canvasContainer = document.getElementById('canvas-container');
    canvasContainer.innerHTML = '';
    
    // Run the super experiment
    try {
        // Set key mappings based on response set relationship
        const keyMappings = {
            identical: {
                movementKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' },
                orientationKeyMap: { 180: 'a', 0: 'd', 90: 'w', 270: 's' }
            }
        };
        
        const config = {
            movementKeyMap: keyMappings.identical.movementKeyMap,
            orientationKeyMap: keyMappings.identical.orientationKeyMap
        };
        
        // End any previous block first
        await superExperiment.endBlock();
        
        // Run single trial block (matching the pattern from experiment.js)
        const data = await superExperiment.block([trial], 2000, config, false, true, null, canvasContainer);
        console.log('Experiment completed. Data:', data);
        
    } catch (error) {
        console.error('Error running experiment:', error);
        console.error('Error stack:', error.stack);
        canvasContainer.innerHTML = '<div style="color: red; padding: 20px;">Error running experiment. Check console for details.</div>';
        
        // Clean up on error
        try {
            await superExperiment.endBlock();
        } catch (cleanupError) {
            console.error('Error during cleanup:', cleanupError);
        }
    }
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
        
        // Filter to only include Telford 1931 experiments (first 4 as requested)
        resolvedData = resolvedData.filter(row => 
            row.Experiment && row.Experiment.startsWith('Telford 1931')
        ).slice(0, 12);
        
        console.log(`Filtered to ${resolvedData.length} Telford 1931 experiments`);
        
        // Populate dropdown
        const select = document.getElementById('experiment-select');
        resolvedData.forEach((row, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = row.Experiment;
            select.appendChild(option);
        });
        
        // Add event listener
        select.addEventListener('change', onExperimentChange);
        
        console.log('App initialized successfully');
        
    } catch (error) {
        console.error('Error initializing app:', error);
        document.getElementById('canvas-container').innerHTML = '<div style="color: red; padding: 20px;">Error loading experiment data. Check console for details.</div>';
    }
}

// Start the app when page loads
document.addEventListener('DOMContentLoaded', initializeApp);

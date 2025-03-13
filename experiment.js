function setupCanvas() {
    // Find the canvas element (it's created by superExperiment)
    const canvas = document.querySelector('canvas');
    if (canvas) {
        // Get our container
        const container = document.getElementById('canvas-container');
        
        // Move the canvas into our container
        container.innerHTML = ''; // Clear any previous canvas
        container.appendChild(canvas);
        
        // Ensure the canvas has the right styling
        canvas.style.position = 'relative';
        canvas.style.zIndex = '10';
    }
}

// Update the timeline drawing function
function drawTimeline(params) {
    const svg = document.getElementById('timeline-svg');
    
    // Clear previous timeline
    svg.innerHTML = '';
    
    // Timeline settings
    const timelineStart = 0;
    const timelineEnd = 7000;  // Extended to 7000ms to show full range
    const margin = { left: 100, right: 20, top: 20, bottom: 30 };
    const width = svg.clientWidth - margin.left - margin.right;
    const height = 200 - margin.top - margin.bottom;
    
    // Create a group for the timeline content with margins
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `translate(${margin.left},${margin.top})`);
    svg.appendChild(g);
    
    // Draw time axis
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", "0");
    axis.setAttribute("y1", "160");
    axis.setAttribute("x2", width);
    axis.setAttribute("y2", "160");
    axis.setAttribute("stroke", "white");
    axis.setAttribute("stroke-width", "2");
    g.appendChild(axis);
    
    // Add time markers every second
    for(let t = 0; t <= timelineEnd; t += 1000) {
        const x = (t * width / timelineEnd);
        
        // Tick mark
        const tick = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tick.setAttribute("x1", x);
        tick.setAttribute("y1", "155");
        tick.setAttribute("x2", x);
        tick.setAttribute("y2", "165");
        tick.setAttribute("stroke", "white");
        tick.setAttribute("stroke-width", "2");
        g.appendChild(tick);
        
        // Label
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", x);
        label.setAttribute("y", "180");
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", "white");
        label.setAttribute("font-size", "12px");
        label.textContent = `${t}ms`;
        g.appendChild(label);
    }
    
    // Draw task components
    function drawComponent(start, duration, yPos, color, label, style = 'solid') {
        const x = start * width / timelineEnd;
        const componentWidth = duration * width / timelineEnd;
        
        // Draw background rectangle for the component
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", yPos);
        rect.setAttribute("width", componentWidth);
        rect.setAttribute("height", "40");
        rect.setAttribute("fill", color);
        rect.setAttribute("opacity", style === 'solid' ? "0.7" : "0.3");
        
        // Add pattern for cue intervals
        if (style === 'cue') {
            rect.setAttribute("stroke", "white");
            rect.setAttribute("stroke-dasharray", "5,5");
        }
        // Add pattern for go intervals
        if (style === 'go') {
            rect.setAttribute("stroke", "yellow");
            rect.setAttribute("stroke-width", "2");
        }
        
        g.appendChild(rect);
        
        // Label (only for main components)
        if (style === 'solid') {
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", -5);
            text.setAttribute("y", yPos + 25);
            text.setAttribute("fill", "white");
            text.setAttribute("text-anchor", "end");
            text.setAttribute("font-size", "14px");
            text.textContent = label;
            g.appendChild(text);
        }
    }
    
    // Draw Task 1 components
    const task1Y = 40;
    // Main stimulus period
    drawComponent(params.start_mov_1, params.dur_mov_1, task1Y, "#f39c12", "Motion Task");
    // Cue period
    drawComponent(params.start_1, params.dur_1, task1Y, "#f39c12", "", "cue");
    // Go period
    drawComponent(params.start_go_1, params.dur_go_1, task1Y, "#f39c12", "", "go");
    
    // Draw Task 2 (distractor) components
    const task2Y = 100;
    if (params.dur_or_2 > 0) {  // Only draw if there's a distractor
        // Distractor stimulus period
        drawComponent(params.start_or_2, params.dur_or_2, task2Y, "#4a90e2", "Orientation Task");
        // No cue or go intervals for distractor
    }
}

function createTrialSequence(numTrials, params, switchRate) {
    const sequence = [];
    let currentTask = 'mov';  // Start with movement task
    
    for (let i = 0; i < numTrials; i++) {
        // Determine if this trial should switch tasks
        if (i > 0 && Math.random() < switchRate) {
            currentTask = currentTask === 'mov' ? 'or' : 'mov';
        }
        
        // Get random directions for motion and orientation
        const mov_dir = Math.random() < 0.5 ? 0 : 180;
        const or_dir = Math.random() < 0.5 ? 90 : 270;

        // Create trial with the paradigm's timing parameters
        const trial = {
            ...params,
            // Switch the task type based on currentTask
            task_1: currentTask,
            // If movement is the current task
            start_mov_1: currentTask === 'mov' ? params.start_mov_1 : 0,
            dur_mov_1: currentTask === 'mov' ? params.dur_mov_1 : 0,
            start_or_1: currentTask === 'or' ? params.start_mov_1 : 0,  // Use same timing as mov_1
            dur_or_1: currentTask === 'or' ? params.dur_mov_1 : 0,
            // Distractor timing
            task_2: currentTask === 'mov' ? 'or' : 'mov',  // Always opposite of task_1
            start_mov_2: currentTask === 'or' ? params.start_or_2 : 0,  // Only active when main task is orientation
            dur_mov_2: currentTask === 'or' ? params.dur_or_2 : 0,
            start_or_2: currentTask === 'mov' ? params.start_or_2 : 0,  // Only active when main task is movement  
            dur_or_2: currentTask === 'mov' ? params.dur_or_2 : 0,
            // Set directions and coherence
            dir_mov_1: mov_dir,
            dir_or_1: or_dir,
            dir_mov_2: mov_dir,
            dir_or_2: or_dir,
            coh_mov_1: 0.25,
            coh_or_1: 0.25,
            coh_mov_2: 0.25,
            coh_or_2: 0.25
        };

        sequence.push(trial);
        console.log(`Trial ${i}: ${currentTask} task, switch probability: ${switchRate}`);
    }

    return sequence;
}

// Convert slider value (0-4) to actual parameter value (0-1)
function sliderToValue(sliderValue) {
    return sliderValue * 0.25;
}

// Generate trial parameters based on current slider values
// TODO: Currently go intervals must match cue intervals for proper cue display.
// This means responses can be made during pre-cue period when stimulus isn't present.
// Future improvement: Decouple go intervals from cue intervals. That would have to
// be done in draw() in package/src/game.js
function generateTrialParams(switchRate, preCueDuration, distractorDuration) {
    const baseDuration = 2000; // Base stimulus duration
    const preCueTime = preCueDuration * baseDuration;
    const distractorTime = distractorDuration * baseDuration;
    const stimulusStart = 3500;  // Fixed stimulus start time
    
    return {
        task_1: 'mov',  // Primary task is movement
        start_1: stimulusStart - preCueTime,  // Cue starts before stimulus
        dur_1: baseDuration + preCueTime,     // Cue spans pre-cue and stimulus period
        start_mov_1: stimulusStart,           // Stimulus timing unchanged
        dur_mov_1: baseDuration,
        start_or_1: 0,
        dur_or_1: 0,
        start_go_1: stimulusStart - preCueTime,            // Go signal matches stimulus
        dur_go_1: baseDuration + preCueTime,
        
        // Second task acts as distractor
        task_2: 'or',
        start_2: 0,
        dur_2: 0,
        start_mov_2: 0,
        dur_mov_2: 0,
        start_or_2: distractorTime > 0 ? stimulusStart : 0,
        dur_or_2: distractorTime > 0 ? distractorTime : 0,
        start_go_2: 0,
        dur_go_2: 0
    };
}

function validateTimingParams(params) {
    if (params.start_1 < 0) {
        console.warn('Warning: Negative cue start time');
    }
    if (params.dur_or_2 > params.dur_mov_1) {
        console.warn('Warning: Distractor duration exceeds main task duration');
    }
}

async function runExperiment(currentParams) {
    try {
        console.log('Cleaning up previous experiment...');
        await superExperiment.endBlock();

        await new Promise(resolve => setTimeout(resolve, 100));
        console.log('Starting new experiment setup...');
        
        const switchRate = sliderToValue(document.getElementById('switch-rate').value);
        validateTimingParams(currentParams);
        const trials = createTrialSequence(5, currentParams, switchRate);
        const config = {
            'size': 0.5,
            'movementKeyMap': {
                180: 'a',
                0: 'd',
                90: 'w',
                270: 's'
            },
            'orientationKeyMap': {
                180: 'a',
                0: 'd',
                90: 'w',
                270: 's'
            },
            'movCueStyle': 'dotted',
            'orCueStyle': 'dashed'
        };

        const canvasContainer = document.getElementById('canvas-container');
        console.log('Starting block with trials...');
        const data = await superExperiment.block(trials, 2000, config, false, true, null, canvasContainer);
        setupCanvas();
        console.log('Block completed. Data:', data);
    } catch (error) {
        console.error('Error in experiment:', error);
        console.error('Error stack:', error.stack);
        await superExperiment.endBlock();
    }
}

// Set up event listeners for sliders and start button
document.addEventListener('DOMContentLoaded', () => {
    const sliders = {
        switchRate: document.getElementById('switch-rate'),
        preCue: document.getElementById('pre-cue'),
        distractor: document.getElementById('distractor')
    };
    
    // Update value displays when sliders change
    Object.entries(sliders).forEach(([key, slider]) => {
        const valueDisplay = document.getElementById(`${slider.id}-value`);
        slider.addEventListener('input', () => {
            valueDisplay.textContent = sliderToValue(slider.value).toFixed(2);
        });
    });
    
    // Handle experiment start
    document.getElementById('start-experiment').addEventListener('click', () => {
        const params = generateTrialParams(
            sliderToValue(sliders.switchRate.value),
            sliderToValue(sliders.preCue.value),
            sliderToValue(sliders.distractor.value)
        );
        
        drawTimeline(params);
        runExperiment(params);
    });
});

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
    const margin = { left: 120, right: 20, top: 20, bottom: 30 }; // Increased left margin for labels
    const width = svg.clientWidth - margin.left - margin.right;
    const height = 280 - margin.top - margin.bottom; // Increased height for four axes
    
    // Create a group for the timeline content with margins
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `translate(${margin.left},${margin.top})`);
    svg.appendChild(g);
    
    // Draw time axis
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", "0");
    axis.setAttribute("y1", height + 10);
    axis.setAttribute("x2", width);
    axis.setAttribute("y2", height + 10);
    axis.setAttribute("stroke", "white");
    axis.setAttribute("stroke-width", "2");
    g.appendChild(axis);
    
    // Add time markers every second
    for(let t = 0; t <= timelineEnd; t += 1000) {
        const x = (t * width / timelineEnd);
        
        // Tick mark
        const tick = document.createElementNS("http://www.w3.org/2000/svg", "line");
        tick.setAttribute("x1", x);
        tick.setAttribute("y1", height + 5);
        tick.setAttribute("x2", x);
        tick.setAttribute("y2", height + 15);
        tick.setAttribute("stroke", "white");
        tick.setAttribute("stroke-width", "2");
        g.appendChild(tick);
        
        // Label
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", x);
        label.setAttribute("y", height + 30);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", "white");
        label.setAttribute("font-size", "12px");
        label.textContent = `${t}ms`;
        g.appendChild(label);
    }
    
    // Define y-positions for the four axes
    const yPositions = {
        motionCue: 40,
        motionStimulus: 90,
        orientationCue: 140,
        orientationStimulus: 190
    };
    
    // Draw axis labels
    function drawAxisLabel(label, yPos) {
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", -10);
        text.setAttribute("y", yPos + 20); // Center text vertically
        text.setAttribute("text-anchor", "end");
        text.setAttribute("fill", "white");
        text.setAttribute("font-size", "14px");
        text.textContent = label;
        g.appendChild(text);
        
        // Add a light horizontal line for the axis
        const axisLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        axisLine.setAttribute("x1", "0");
        axisLine.setAttribute("y1", yPos + 20);
        axisLine.setAttribute("x2", width);
        axisLine.setAttribute("y2", yPos + 20);
        axisLine.setAttribute("stroke", "rgba(255,255,255,0.2)");
        axisLine.setAttribute("stroke-width", "1");
        axisLine.setAttribute("stroke-dasharray", "3,3");
        g.appendChild(axisLine);
    }
    
    // Draw the four axis labels
    drawAxisLabel("Motion Cue", yPositions.motionCue);
    drawAxisLabel("Motion Stimulus", yPositions.motionStimulus);
    drawAxisLabel("Orientation Cue", yPositions.orientationCue);
    drawAxisLabel("Orientation Stimulus", yPositions.orientationStimulus);
    
    // Draw task components
    function drawComponent(start, duration, yPos, color, style = 'solid') {
        if (duration <= 0) return; // Don't draw components with zero duration
        
        const x = start * width / timelineEnd;
        const componentWidth = Math.max(2, duration * width / timelineEnd); // Ensure minimum width for visibility
        
        // Create a group for this component
        const componentGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.appendChild(componentGroup);
        
        // Draw background rectangle for the component
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", yPos);
        rect.setAttribute("width", componentWidth);
        rect.setAttribute("height", "40");
        rect.setAttribute("fill", color);
        rect.setAttribute("opacity", "0.7");
        componentGroup.appendChild(rect);
        
        // Add specialized styling based on component type
        if (style === 'go') {
            // Add yellow border for go signals
            rect.setAttribute("stroke", "yellow");
            rect.setAttribute("stroke-width", "2");
        }
        
        // Add start/end time labels for components with significant duration
        if (duration >= 500) {
            // Start time label
            const startLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
            startLabel.setAttribute("x", x + 5);
            startLabel.setAttribute("y", yPos + 15);
            startLabel.setAttribute("fill", "white");
            startLabel.setAttribute("font-size", "10px");
            startLabel.textContent = `${start}ms`;
            componentGroup.appendChild(startLabel);
            
            // End time label if there's enough space
            if (componentWidth > 60) {
                const endLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
                endLabel.setAttribute("x", x + componentWidth - 5);
                endLabel.setAttribute("y", yPos + 15);
                endLabel.setAttribute("text-anchor", "end");
                endLabel.setAttribute("fill", "white");
                endLabel.setAttribute("font-size", "10px");
                endLabel.textContent = `${start + duration}ms`;
                componentGroup.appendChild(endLabel);
            }
        }
    }
    
    // Draw motion task components
    if (params.task_1 === 'mov' || params.task_2 === 'mov') {
        // Motion cue
        if (params.task_1 === 'mov') {
            drawComponent(params.start_1, params.dur_1, yPositions.motionCue, "#f39c12");
        } else if (params.task_2 === 'mov') {
            drawComponent(params.start_2, params.dur_2, yPositions.motionCue, "#f39c12");
        }
        
        // Motion stimulus
        if (params.task_1 === 'mov') {
            drawComponent(params.start_mov_1, params.dur_mov_1, yPositions.motionStimulus, "#e67e22");
            drawComponent(params.start_go_1, params.dur_go_1, yPositions.motionStimulus, "#e67e22", "go");
        } else if (params.task_2 === 'mov') {
            drawComponent(params.start_mov_2, params.dur_mov_2, yPositions.motionStimulus, "#e67e22");
            drawComponent(params.start_go_2, params.dur_go_2, yPositions.motionStimulus, "#e67e22", "go");
        }
    }
    
    // Draw orientation task components
    if (params.task_1 === 'or' || params.task_2 === 'or') {
        // Orientation cue
        if (params.task_1 === 'or') {
            drawComponent(params.start_1, params.dur_1, yPositions.orientationCue, "#4a90e2");
        } else if (params.task_2 === 'or') {
            drawComponent(params.start_2, params.dur_2, yPositions.orientationCue, "#4a90e2");
        }
        
        // Orientation stimulus
        if (params.task_1 === 'or') {
            drawComponent(params.start_or_1, params.dur_or_1, yPositions.orientationStimulus, "#3498db");
            drawComponent(params.start_go_1, params.dur_go_1, yPositions.orientationStimulus, "#3498db", "go");
        } else if (params.task_2 === 'or') {
            drawComponent(params.start_or_2, params.dur_or_2, yPositions.orientationStimulus, "#3498db");
            drawComponent(params.start_go_2, params.dur_go_2, yPositions.orientationStimulus, "#3498db", "go");
        }
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
        
        setupCanvas(); // Call setupCanvas once before starting trials
        
        for (let i = 0; i < trials.length; i++) {
            const trial = trials[i];
            await superExperiment.endBlock();
            drawTimeline(trial); // Update the timeline for the current trial
            const data = await superExperiment.block([trial], 2000, config, false, true, null, canvasContainer);
        }
        
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

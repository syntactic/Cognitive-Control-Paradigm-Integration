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
        const componentWidth = Math.max(2, duration * width / timelineEnd);
        
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
        
        // Make cue periods more transparent than stimulus periods
        if (style === 'cue') {
            rect.setAttribute("opacity", "0.3");
        } else if (style === 'go') {
            rect.setAttribute("fill-opacity", "0.0");
        } else {
            rect.setAttribute("opacity", "0.7");
        }
        
        componentGroup.appendChild(rect);
        
        // Add specialized styling based on component type
        if (style === 'go') {
            rect.setAttribute("stroke", "yellow");
            rect.setAttribute("stroke-width", "2");
        }
        
        // Add start/end time labels for components with significant duration
        if (duration >= 500) {
            const startLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
            startLabel.setAttribute("x", x + 5);
            startLabel.setAttribute("y", yPos + 15);
            startLabel.setAttribute("fill", "white");
            startLabel.setAttribute("font-size", "10px");
            startLabel.textContent = `${start}ms`;
            componentGroup.appendChild(startLabel);
            
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
    
    // Determine if we have a dual-task paradigm
    // TODO double check the logic here
    const isDualTask = params.task_1 && params.task_2 && 
                     ((params.dur_mov_1 > 0 && params.dur_or_2 > 0) || 
                      (params.dur_or_1 > 0 && params.dur_mov_2 > 0));
    
    // If it's a dual-task paradigm, draw a visual separator for SOA
    if (isDualTask) {
        // Calculate SOA
        let soaStart = 0;
        let soaEnd = 0;
        
        if (params.task_1 === 'mov' && params.task_2 === 'or') {
            soaStart = params.start_mov_1;
            soaEnd = params.start_or_2;
        } else if (params.task_1 === 'or' && params.task_2 === 'mov') {
            soaStart = params.start_or_1;
            soaEnd = params.start_mov_2;
        }
        
        if (soaStart !== soaEnd) {
            // Draw SOA indicator
            const soaX1 = soaStart * width / timelineEnd;
            const soaX2 = soaEnd * width / timelineEnd;
            
            // Draw SOA line
            const soaLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
            soaLine.setAttribute("x1", soaX1);
            soaLine.setAttribute("y1", 10);
            soaLine.setAttribute("x2", soaX2);
            soaLine.setAttribute("y2", 10);
            soaLine.setAttribute("stroke", "#FF5722");
            soaLine.setAttribute("stroke-width", "3");
            g.appendChild(soaLine);
            
            // Add SOA label
            const soaLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
            soaLabel.setAttribute("x", (soaX1 + soaX2) / 2);
            soaLabel.setAttribute("y", 8);
            soaLabel.setAttribute("text-anchor", "middle");
            soaLabel.setAttribute("fill", "#FF5722");
            soaLabel.setAttribute("font-size", "12px");
            soaLabel.textContent = `SOA: ${Math.abs(soaEnd - soaStart)}ms`;
            g.appendChild(soaLabel);
        }
    }
    
    // Draw motion task components
    if (params.task_1 === 'mov' || params.task_2 === 'mov') {
        // Motion cue
        if (params.task_1 === 'mov') {
            drawComponent(params.start_1, params.dur_1, yPositions.motionCue, "#f39c12");
            // Motion stimulus
            drawComponent(params.start_mov_1, params.dur_mov_1, yPositions.motionStimulus, "#e67e22");
            drawComponent(params.start_go_1, params.dur_go_1, yPositions.motionCue, "#e67e22", "go");
        }
        
        if (params.task_2 === 'mov') {
            drawComponent(params.start_2, params.dur_2, yPositions.motionCue, "#f39c12");
            // Motion stimulus
            drawComponent(params.start_mov_2, params.dur_mov_2, yPositions.motionStimulus, "#e67e22");
            drawComponent(params.start_go_2, params.dur_go_2, yPositions.motionCue, "#e67e22", "go");
        }
    }
    
    // Draw orientation task components
    if (params.task_1 === 'or' || params.task_2 === 'or') {
        // Orientation cue
        if (params.task_1 === 'or') {
            drawComponent(params.start_1, params.dur_1, yPositions.orientationCue, "#4a90e2");
            // Orientation stimulus
            drawComponent(params.start_or_1, params.dur_or_1, yPositions.orientationStimulus, "#3498db");
            drawComponent(params.start_go_1, params.dur_go_1, yPositions.orientationCue, "#3498db", "go");
        }
        
        if (params.task_2 === 'or') {
            drawComponent(params.start_2, params.dur_2, yPositions.orientationCue, "#4a90e2");
            // Orientation stimulus
            drawComponent(params.start_or_2, params.dur_or_2, yPositions.orientationStimulus, "#3498db");
            drawComponent(params.start_go_2, params.dur_go_2, yPositions.orientationCue, "#3498db", "go");
        }
    }
    
    // If this is a dual-task paradigm, add a label
    if (isDualTask) {
        const paradigmLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
        paradigmLabel.setAttribute("x", width / 2);
        paradigmLabel.setAttribute("y", height + 50);
        paradigmLabel.setAttribute("text-anchor", "middle");
        paradigmLabel.setAttribute("fill", "white");
        paradigmLabel.setAttribute("font-size", "14px");
        paradigmLabel.setAttribute("font-weight", "bold");
        
        // Determine paradigm type
        let paradigmType = "Dual-Task";
        if (params.start_mov_1 > 0 && params.start_or_2 > 0) {
            const soa = params.start_or_2 - params.start_mov_1;
            if (soa <= 50) {
                paradigmType = "Full Dual-Task";
            } else if (soa < 300) {
                paradigmType = "Psychological Refractory Period (PRP) - Short SOA";
            } else if (soa < 1000) {
                paradigmType = "Psychological Refractory Period (PRP) - Medium SOA";
            } else {
                paradigmType = "Sequential Task Processing";
            }
        }
        
        paradigmLabel.textContent = paradigmType;
        g.appendChild(paradigmLabel);
    }
}

function createTrialSequence(numTrials, params, switchRate) {
    const sequence = [];
    let currentTask = 'mov';  // Start with movement task
    
    // Check if this is a dual-task paradigm - both tasks should be active
    const isDualTask = params.dur_1 > 0 && params.dur_2 > 0;
    
    for (let i = 0; i < numTrials; i++) {
        // Determine if this trial should switch tasks (only for single-task paradigm)
        if (!isDualTask && i > 0 && Math.random() < switchRate) {
            currentTask = currentTask === 'mov' ? 'or' : 'mov';
        }
        
        // Get random directions for motion and orientation
        const mov_dir = Math.random() < 0.5 ? 0 : 180;
        const or_dir = Math.random() < 0.5 ? 90 : 270;

        // Create trial with the paradigm's timing parameters
        let trial;
        
        if (isDualTask) {
            // For dual-task paradigms, use the parameters directly
            // Both tasks are active and should run according to their specified timing
            trial = {
                ...params,
                // Set directions and coherence for both tasks
                dir_mov_1: mov_dir,
                dir_or_1: or_dir,
                dir_mov_2: mov_dir,
                dir_or_2: or_dir,
                coh_mov_1: 0.25,
                coh_or_1: 0.25,
                coh_mov_2: 0.25,
                coh_or_2: 0.25
            };
        } else {
            // For single-task paradigms, adjust parameters based on current task
            trial = {
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
        }

        sequence.push(trial);
        
        if (isDualTask) {
            console.log(`Trial ${i}: Dual-task paradigm with both motion and orientation tasks`);
        } else {
            console.log(`Trial ${i}: ${currentTask} task, switch probability: ${switchRate}`);
        }
    }

    return sequence;
}

// Convert slider value (0-4) to actual parameter value (0-1)
function sliderToValue(sliderValue) {
    return sliderValue * 0.25;
}

// Generate trial parameters for single-task/task-switching paradigms
// TODO: Currently go intervals must match cue intervals for proper cue display.
// This means responses can be made during pre-cue period when stimulus isn't present.
// Future improvement: Decouple go intervals from cue intervals. That would have to
// be done in draw() in package/src/game.js
function generateTrialParams(switchRate, preCueDuration, distractorDuration) {
    const baseDuration = 2000; // Base stimulus duration
    const preCueTime = preCueDuration * baseDuration;
    const distractorTime = distractorDuration * baseDuration;
    const stimulusStart = 3500;  // Fixed stimulus start time
    
    // Update the timing parameters to correctly reflect the stimulus timing
    return {
        task_1: 'mov',  // Primary task is movement
        start_1: stimulusStart - preCueTime,  // Cue starts before stimulus
        dur_1: baseDuration + preCueTime,     // Cue spans pre-cue and stimulus period
        start_mov_1: stimulusStart,           // Stimulus starts at 3500ms
        dur_mov_1: baseDuration,
        start_or_1: 0,
        dur_or_1: 0,
        start_go_1: stimulusStart - preCueTime,  // Go signal matches cue timing
        dur_go_1: baseDuration + preCueTime,
        
        // Second task acts as distractor
        task_2: 'or',
        start_2: 0,
        dur_2: 0,
        start_mov_2: 0,
        dur_mov_2: 0,
        start_or_2: distractorTime > 0 ? stimulusStart : 0,  // Distractor starts with main stimulus
        dur_or_2: distractorTime > 0 ? distractorTime : 0,
        start_go_2: 0,
        dur_go_2: 0
    };
}

// Generate trial parameters for dual-task/PRP paradigms
function generateDualTaskParams(temporalSeparation, cueReduction, preCueDuration) {
    const baseDuration = 2000; // Base stimulus duration
    const stimulusStart = 1500;  // Fixed stimulus start time
    
    // Calculate SOA based on temporal separation
    const soaTime = baseDuration * temporalSeparation;
    
    // Handle mutual exclusivity between pre-cue and cue reduction
    let preCueTime = 0;
    let cueReductionTime = 0;
    
    if (cueReduction > 0) {
        cueReductionTime = cueReduction * baseDuration;
        preCueTime = 0;
    } else {
        preCueTime = preCueDuration * baseDuration;
        cueReductionTime = 0;
    }
    
    // Determine paradigm type for visualization/logging purposes
    let paradigmType;
    if (temporalSeparation < 0.05) paradigmType = "FULL_DUAL_TASK";
    else if (temporalSeparation < 0.3) paradigmType = "PRP_SHORT";
    else if (temporalSeparation < 0.6) paradigmType = "PRP_MEDIUM";
    else paradigmType = "PRP_LONG";
    
    console.log(`Generating ${paradigmType} paradigm with SOA=${soaTime}ms`);
    
    // Create the parameters with unified logic
    return {
        // First task (movement)
        task_1: 'mov',
        start_1: stimulusStart - preCueTime,
        dur_1: baseDuration + preCueTime,
        start_mov_1: stimulusStart,
        dur_mov_1: baseDuration,
        start_or_1: 0,
        dur_or_1: 0,
        start_go_1: stimulusStart - preCueTime,
        dur_go_1: baseDuration + preCueTime,
        
        // Second task (orientation)
        task_2: 'or',
        start_2: cueReductionTime > 0 
            ? stimulusStart + soaTime + cueReductionTime
            : (stimulusStart + soaTime) - preCueTime,
        dur_2: cueReductionTime > 0 
            ? baseDuration - cueReductionTime
            : baseDuration + preCueTime,
        start_mov_2: 0,
        dur_mov_2: 0,
        start_or_2: stimulusStart + soaTime,
        dur_or_2: baseDuration,
        start_go_2: cueReductionTime > 0 
            ? stimulusStart + soaTime + cueReductionTime
            : (stimulusStart + soaTime) - preCueTime,
        dur_go_2: cueReductionTime > 0 
            ? baseDuration - cueReductionTime
            : baseDuration + preCueTime
    };
}

function validateTimingParams(params) {
    // Validate dual-task parameters
    const isDualTask = params.task_1 && params.task_2 && 
                     ((params.dur_mov_1 > 0 && params.dur_or_2 > 0) || 
                      (params.dur_or_1 > 0 && params.dur_mov_2 > 0));
    
    if (params.start_1 < 0) {
        console.warn('Warning: Negative cue start time for task 1');
    }
    
    if (params.start_2 < 0) {
        console.warn('Warning: Negative cue start time for task 2');
    }
    
    if (!isDualTask && params.dur_or_2 > params.dur_mov_1) {
        console.warn('Warning: Distractor duration exceeds main task duration');
    }
    
    if (isDualTask) {
        // Check if both tasks have appropriate parameters set
        if (params.task_1 === 'mov' && params.dur_mov_1 <= 0) {
            console.warn('Warning: Task 1 is movement but duration is zero or negative');
        }
        
        if (params.task_1 === 'or' && params.dur_or_1 <= 0) {
            console.warn('Warning: Task 1 is orientation but duration is zero or negative');
        }
        
        if (params.task_2 === 'mov' && params.dur_mov_2 <= 0) {
            console.warn('Warning: Task 2 is movement but duration is zero or negative');
        }
        
        if (params.task_2 === 'or' && params.dur_or_2 <= 0) {
            console.warn('Warning: Task 2 is orientation but duration is zero or negative');
        }
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
    // Setup paradigm type radio buttons
    const paradigmRadios = document.querySelectorAll('input[name="paradigm-type"]');
    const singleTaskParams = document.getElementById('single-task-parameters');
    const dualTaskParams = document.getElementById('dual-task-parameters');
    
    // Enable both radio buttons
    paradigmRadios.forEach(radio => {
        radio.disabled = false;
        radio.addEventListener('change', () => {
            if (radio.value === 'single-task') {
                singleTaskParams.style.display = 'flex';
                dualTaskParams.style.display = 'none';
            } else if (radio.value === 'dual-task') {
                singleTaskParams.style.display = 'none';
                dualTaskParams.style.display = 'flex';
            }
        });
    });
    
    // Configure single-task sliders
    const singleTaskSliders = {
        switchRate: document.getElementById('switch-rate'),
        preCue: document.getElementById('pre-cue'),
        distractor: document.getElementById('distractor')
    };
    
    // Configure dual-task sliders
    const dualTaskSliders = {
        temporalSeparation: document.getElementById('temporal-separation'),
        cueReduction: document.getElementById('second-task-cue-reduction'),
        preCue: document.getElementById('dual-pre-cue')
    };

    function updateValueDisplay(slider) {
        const valueDisplay = document.getElementById(`${slider.id}-value`);
        valueDisplay.textContent = sliderToValue(slider.value).toFixed(2);
    }
    
    // Update value displays when sliders change for single-task paradigms
    Object.entries(singleTaskSliders).forEach(([key, slider]) => {
        slider.addEventListener('input', () => {
            updateValueDisplay(slider);
        });
        updateValueDisplay(slider);
    });
    
    // Update value displays when sliders change for dual-task paradigms
    Object.entries(dualTaskSliders).forEach(([key, slider]) => {
        slider.addEventListener('input', () => {
            updateValueDisplay(slider);
            
            // Implement mutual exclusivity between pre-cue and cue reduction
            if (key === 'cueReduction' && sliderToValue(slider.value) > 0) {
                // If cue reduction is active, disable pre-cue
                dualTaskSliders.preCue.value = 0;
                updateValueDisplay(dualTaskSliders.preCue);
                dualTaskSliders.preCue.disabled = true;
            } else if (key === 'cueReduction' && sliderToValue(slider.value) === 0) {
                // Re-enable pre-cue when cue reduction is zero
                dualTaskSliders.preCue.disabled = false;
            }
            
            if (key === 'preCue' && sliderToValue(slider.value) > 0) {
                // If pre-cue is active, disable cue reduction
                dualTaskSliders.cueReduction.value = 0;
                updateValueDisplay(dualTaskSliders.cueReduction);
                dualTaskSliders.cueReduction.disabled = true;
            } else if (key === 'preCue' && sliderToValue(slider.value) === 0) {
                // Re-enable cue reduction when pre-cue is zero
                dualTaskSliders.cueReduction.disabled = false;
            }
        });
        updateValueDisplay(slider);
    });
    
    // Handle experiment start
    document.getElementById('start-experiment').addEventListener('click', () => {
        // Get selected paradigm type
        const paradigmType = document.querySelector('input[name="paradigm-type"]:checked').value;
        
        let params;
        if (paradigmType === 'single-task') {
            params = generateTrialParams(
                sliderToValue(singleTaskSliders.switchRate.value),
                sliderToValue(singleTaskSliders.preCue.value),
                sliderToValue(singleTaskSliders.distractor.value)
            );
        } else if (paradigmType === 'dual-task') {
            params = generateDualTaskParams(
                sliderToValue(dualTaskSliders.temporalSeparation.value),
                sliderToValue(dualTaskSliders.cueReduction.value),
                sliderToValue(dualTaskSliders.preCue.value)
            );
        }
        
        drawTimeline(params);
        runExperiment(params);
    });
});

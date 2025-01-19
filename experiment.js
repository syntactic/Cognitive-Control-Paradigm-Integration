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
function drawTimeline(paradigm) {
    const svg = document.getElementById('timeline-svg');
    const params = PARADIGMS[paradigm].params;
    
    // Clear previous timeline
    svg.innerHTML = '';
    
    // Timeline settings
    const timelineStart = 0;
    const timelineEnd = 7000;  // Extended to 7000ms to show full range
    const margin = { left: 80, right: 20, top: 20, bottom: 30 };
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
    function drawComponent(start, duration, yPos, color, label) {
        const x = start * width / timelineEnd;
        const componentWidth = duration * width / timelineEnd;
        
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", yPos);
        rect.setAttribute("width", componentWidth);
        rect.setAttribute("height", "40");
        rect.setAttribute("fill", color);
        rect.setAttribute("opacity", "0.7");
        
        g.appendChild(rect);
        
        // Label
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", -5);
        text.setAttribute("y", yPos + 25);
        text.setAttribute("fill", "white");
        text.setAttribute("text-anchor", "end");
        text.setAttribute("font-size", "14px");
        text.textContent = label;
        g.appendChild(text);
    }
    
    // Draw Task 1 - combining cue and signal periods
    const task1Start = Math.min(params.start_1, params.start_mov_1);
    const task1End = Math.max(params.start_1 + params.dur_1, params.start_mov_1 + params.dur_mov_1);
    drawComponent(task1Start, task1End - task1Start, 40, "#f39c12", "Task 1");
    
    // Draw Task 2 - combining cue and signal periods
    const task2Start = params.start_2;
    const task2End = params.start_2 + params.dur_2;
    drawComponent(task2Start, task2End - task2Start, 100, "#4a90e2", "Task 2");
}
const overlap_paradigm = {
    params: {
        // First task (Movement)
        task_1: 'mov',
        start_1: 0,
        dur_1: 3000,         // First 3s
        start_mov_1: 0,
        dur_mov_1: 3000,     // Motion for first 3s
        start_or_1: 2000,    // Start orientation at 2s
        dur_or_1: 1000,      // Overlap for 1s
        start_go_1: 0,
        dur_go_1: 3000,
        
        // Second task (Orientation)
        task_2: 'or',
        start_2: 2000,        // Start at 2s
        dur_2: 3000,          // Last for 3s
        start_mov_2: -1000,   // Adjusted for addTime
        dur_mov_2: 1000,      // Duration of overlap
        start_or_2: 0,    // Adjusted for addTime
        dur_or_2: 2000,       // Full orientation duration
        start_go_2: 2000,
        dur_go_2: 3000
    }
};
const PARADIGMS = {
    sequential: {
        name: "Pure Sequential Task Switching",
        params: {
            // First task (Movement)
            task_1: 'mov',
            start_1: 0,
            dur_1: 3000,
            start_mov_1: 0,
            dur_mov_1: 3000,
            start_or_1: 0,
            dur_or_1: 0,      // No orientation during first task
            start_go_1: 0,
            dur_go_1: 3000,
            
            // Second task (Orientation)
            task_2: 'or',
            start_2: 3500,    // 500ms gap between tasks
            dur_2: 3000,
            start_mov_2: 0,   // No movement during second task
            dur_mov_2: 0,
            start_or_2: 3500,    // Will get shifted by 3000
            dur_or_2: 3000,
            start_go_2: 3500,
            dur_go_2: 3000
        }
    },
    
    minimal_overlap: {
        name: "Minimal Temporal Overlap",
        params: {
            task_1: 'mov',
            start_1: 0,
            dur_1: 3000,
            start_mov_1: 0,
            dur_mov_1: 3000,
            start_or_1: 2500,    // Brief 500ms overlap
            dur_or_1: 500,
            start_go_1: 0,
            dur_go_1: 3000,
            
            task_2: 'or',
            start_2: 2500,
            dur_2: 3000,
            start_mov_2: -500,   // Brief overlap
            dur_mov_2: 500,
            start_or_2: 0,
            dur_or_2: 2500,
            start_go_2: 2500,
            dur_go_2: 3000
        }
    },
    
    substantial_overlap: {
        name: "Substantial Temporal Overlap",
        params: {
            task_1: 'mov',
            start_1: 0,
            dur_1: 3000,
            start_mov_1: 0,
            dur_mov_1: 3000,
            start_or_1: 2000,    // 1s overlap
            dur_or_1: 1000,
            start_go_1: 0,
            dur_go_1: 3000,
            
            task_2: 'or',
            start_2: 2000,
            dur_2: 3000,
            start_mov_2: -1000,
            dur_mov_2: 1000,
            start_or_2: 0,
            dur_or_2: 2000,
            start_go_2: 2000,
            dur_go_2: 3000
        }
    },
    
    dual_task: {
        name: "Full Dual-Task Processing",
        params: {
            task_1: 'mov',
            start_1: 0,
            dur_1: 3000,
            start_mov_1: 0,
            dur_mov_1: 3000,
            start_or_1: 0,       // Complete overlap
            dur_or_1: 3000,
            start_go_1: 0,
            dur_go_1: 3000,
            
            task_2: 'or',
            start_2: 0,
            dur_2: 3000,
            start_mov_2: -3000,
            dur_mov_2: 3000,
            start_or_2: 0,
            dur_or_2: 0,
            start_go_2: 0,
            dur_go_2: 3000
        }
    }
};

function createTrialSequence(numTrials, params) {
    const sequence = [];
    
    for (let i = 0; i < numTrials; i++) {
        // Get random directions for motion and orientation
        // 0 = left, 180 = right
        const mov_dir = Math.random() < 0.5 ? 0 : 180;
        const or_dir = Math.random() < 0.5 ? 90 : 270;

        // Create trial with the paradigm's timing parameters
        const trial = {
		...params,
		'dir_mov_1': mov_dir,
		'dir_or_1': or_dir,
		'dir_mov_2': mov_dir,
		'dir_or_2': or_dir,
		// Set coherence to 1 for all signals
		'coh_mov_1': 0.5,
		'coh_or_1': 0.5,
		'coh_mov_2': 0.5,
		'coh_or_2': 0.5
            };

        sequence.push(trial);
	// Log trial directions for debugging
	console.log(`Trial ${i} directions:`, {
            movement: mov_dir,    // Log single direction
            orientation: or_dir    // Log single direction
        });
    }

    return sequence;

}

async function runExperiment(currentParadigm) {
    try {
        console.log('Cleaning up previous experiment...');
        await superExperiment.endBlock();

        await new Promise(resolve => setTimeout(resolve, 100));
        console.log('Starting new experiment setup...');
        
        const params = PARADIGMS[currentParadigm].params;
        const trials = createTrialSequence(5, params);
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
        
        // Add this line to move the canvas after it's created
        setupCanvas();
        
        console.log('Block completed. Data:', data);
    } catch (error) {
        console.error('Error in experiment:', error);
        console.error('Error stack:', error.stack);
        await superExperiment.endBlock();
    }
}


document.querySelectorAll('.paradigm-button').forEach(button => {
    button.addEventListener('click', async () => {
        const paradigm = button.dataset.paradigm;
        console.log(`Starting ${paradigm} paradigm...`);
        drawTimeline(paradigm);  // Add this line
        await runExperiment(paradigm);
    });
});

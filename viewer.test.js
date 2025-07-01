// viewer.test.js

const { 
    generateITI, 
    convertAbsoluteToSEParams, 
    generateTrialDirections, 
    generateTaskSequence, 
    generateTaskAssignmentSequence,
    createTrialSequence 
} = require('./viewer.js');

describe('generateITI', () => {
    test('should return the fixed ITI value when the distribution type is "fixed"', () => {
        const condition = {
            ITI_Distribution_Type: 'fixed',
            ITI_ms: '1200'
        };
        expect(generateITI(condition)).toBe(1200);
    });

    test('should return a value within the specified range for a "uniform" distribution', () => {
        const condition = {
            ITI_Distribution_Type: 'uniform',
            ITI_Distribution_Params: '[500, 600]'
        };
        const result = generateITI(condition);
        expect(result).toBeGreaterThanOrEqual(500);
        expect(result).toBeLessThanOrEqual(600);
    });

    test('should return a value from the choice array for "choice" distribution', () => {
        const condition = {
            ITI_Distribution_Type: 'choice',
            ITI_Distribution_Params: '[800, 1000, 1200]'
        };
        const result = generateITI(condition);
        expect([800, 1000, 1200]).toContain(result);
    });

    test('should gracefully fall back to default when ITI_ms is not a number', () => {
        const condition = {
            ITI_Distribution_Type: 'fixed',
            ITI_ms: 'invalid'
        };
        const result = generateITI(condition);
        expect(result).toBe(1000); // Default fallback
    });

    test('should gracefully fall back to base ITI when ITI_Distribution_Params is invalid JSON', () => {
        const condition = {
            ITI_Distribution_Type: 'uniform',
            ITI_ms: '1500',
            ITI_Distribution_Params: 'invalid json'
        };
        const result = generateITI(condition);
        expect(result).toBe(1500); // Falls back to base ITI
    });

    test('should default to 1000ms when no ITI_ms is provided', () => {
        const condition = {
            ITI_Distribution_Type: 'fixed'
        };
        const result = generateITI(condition);
        expect(result).toBe(1000);
    });

    test('should default to fixed distribution when no distribution type is provided', () => {
        const condition = {
            ITI_ms: '800'
        };
        const result = generateITI(condition);
        expect(result).toBe(800);
    });
});

describe('convertAbsoluteToSEParams', () => {
    test('should convert absolute timing data to SE parameters for dual-task condition', () => {
        const absoluteRow = {
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '0',  // Unused for dual-task
            effective_end_stim1_or: '0',    // Unused for dual-task
            effective_start_stim2_or: '200', // Channel 2 orientation task
            effective_end_stim2_or: '700',   // Channel 2 orientation task
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '150',
            effective_end_cue2: '200',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '200',
            effective_end_go2: '250',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = convertAbsoluteToSEParams(absoluteRow);

        // Test basic structure
        expect(result.task_1).toBe('mov');
        expect(result.task_2).toBe('or');

        // Test CORRECT dual-task architecture: 
        // Channel 1 gets movement task, Channel 2 gets orientation task
        expect(result.dur_mov_1).toBe(500); // 600 - 100 (Channel 1 movement)
        expect(result.dur_or_1).toBe(0);    // Channel 1 orientation unused in dual-task
        expect(result.dur_mov_2).toBe(0);   // Channel 2 movement unused in dual-task
        expect(result.dur_or_2).toBe(500);  // 700 - 200 (Channel 2 orientation)

        // Test stimulus start times
        expect(result.start_mov_1).toBe(100);
        expect(result.start_or_1).toBe(0);
        expect(result.start_mov_2).toBe(0);
        expect(result.start_or_2).toBe(200);

        // Test cue timings
        expect(result.start_1).toBe(0);
        expect(result.dur_1).toBe(50);
        expect(result.start_2).toBe(150);
        expect(result.dur_2).toBe(50);

        // Test coherence values
        expect(result.coh_1).toBe(0.8);
        expect(result.coh_2).toBe(0.6);
        expect(result.coh_mov_1).toBe(0.8);
        expect(result.coh_or_1).toBe(0);
        expect(result.coh_mov_2).toBe(0);
        expect(result.coh_or_2).toBe(0.6);
    });

    test('should correctly assign dual-task pathways with proper Channel 2 data', () => {
        // This test verifies the CORRECT dual-task implementation
        const absoluteRow = {
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '0',  // Unused for dual-task
            effective_end_stim1_or: '0',    // Unused for dual-task
            effective_start_stim2_or: '200', // Channel 2 orientation task
            effective_end_stim2_or: '700',   // Channel 2 orientation task
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '150',
            effective_end_cue2: '200',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '200',
            effective_end_go2: '250',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = convertAbsoluteToSEParams(absoluteRow);

        // Verify the correct dual-task Channel 2 assignment
        expect(result.start_or_2).toBe(200); // Channel 2 orientation start time
        expect(result.dur_or_2).toBe(500);   // Channel 2 orientation duration
        expect(result.task_2).toBe('or');    // Task 2 should be orientation
    });
});

describe('generateTrialDirections', () => {
    test('should generate congruent directions for single-task Bivalent-Congruent condition', () => {
        const condition = {
            N_Tasks: 1,
            Stimulus_Valency: 'Bivalent-Congruent',
            Simplified_RSO: 'Identical'
        };
        const trialAssignment = { currentTask: 'mov' };

        // Run multiple times to test randomness and consistency
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition, trialAssignment);
            
            // Both Channel 1 directions should be the same for congruent condition
            expect(result.dir_mov_1).toBe(result.dir_or_1);
            expect([0, 180]).toContain(result.dir_mov_1);
            expect([0, 180]).toContain(result.dir_or_1);
            
            // Channel 2 should be inactive
            expect(result.dir_mov_2).toBeNull();
            expect(result.dir_or_2).toBeNull();
        }
    });

    test('should generate incongruent directions for single-task Bivalent-Incongruent condition', () => {
        const condition = {
            N_Tasks: 1,
            Stimulus_Valency: 'Bivalent-Incongruent',
            Simplified_RSO: 'Identical'
        };
        const trialAssignment = { currentTask: 'mov' };

        // Run multiple times to test randomness and consistency
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition, trialAssignment);
            
            // Channel 1 directions should be opposite for incongruent condition
            expect(result.dir_mov_1).not.toBe(result.dir_or_1);
            expect([0, 180]).toContain(result.dir_mov_1);
            expect([0, 180]).toContain(result.dir_or_1);
            
            // Specifically test opposition
            if (result.dir_mov_1 === 0) {
                expect(result.dir_or_1).toBe(180);
            } else {
                expect(result.dir_or_1).toBe(0);
            }
            
            // Channel 2 should be inactive
            expect(result.dir_mov_2).toBeNull();
            expect(result.dir_or_2).toBeNull();
        }
    });

    test('should generate orthogonal directions for single-task Bivalent-Neutral condition', () => {
        const condition = {
            N_Tasks: 1,
            Stimulus_Valency: 'Bivalent-Neutral',
            Simplified_RSO: 'Identical'
        };
        const trialAssignment = { currentTask: 'mov' };

        // Run multiple times to test randomness
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition, trialAssignment);
            
            // Movement should be horizontal (0 or 180)
            expect([0, 180]).toContain(result.dir_mov_1);
            // Orientation should be vertical (90 or 270)
            expect([90, 270]).toContain(result.dir_or_1);
            
            // Channel 2 should be inactive
            expect(result.dir_mov_2).toBeNull();
            expect(result.dir_or_2).toBeNull();
        }
    });

    test('should generate random directions for single-task Univalent condition', () => {
        const condition = {
            N_Tasks: 1,
            Stimulus_Valency: 'Univalent',
            Simplified_RSO: 'Identical'
        };
        const trialAssignment = { currentTask: 'mov' };

        const result = generateTrialDirections(condition, trialAssignment);
        
        // Only movement pathway should be active for univalent mov task
        expect([0, 180]).toContain(result.dir_mov_1);
        expect(result.dir_or_1).toBeNull();
        
        // Channel 2 should be inactive
        expect(result.dir_mov_2).toBeNull();
        expect(result.dir_or_2).toBeNull();
    });

    test('should generate directions for dual-task with disjoint response sets', () => {
        const condition = {
            N_Tasks: 2,
            Stimulus_Valency: 'Univalent',
            Simplified_RSO: 'Disjoint'
        };
        const trialAssignment = { channel1_task: 'mov', channel2_task: 'or' };

        const result = generateTrialDirections(condition, trialAssignment);
        
        // Channel 1 movement task should be active
        expect([0, 180]).toContain(result.dir_mov_1);
        expect(result.dir_or_1).toBeNull();
        
        // Channel 2 orientation task should be active with orthogonal directions
        expect([90, 270]).toContain(result.dir_or_2);
        expect(result.dir_mov_2).toBeNull();
    });

    test('should generate directions for dual-task with identical response sets', () => {
        const condition = {
            N_Tasks: 2,
            Stimulus_Valency: 'Univalent',
            Simplified_RSO: 'Identical'
        };
        const trialAssignment = { channel1_task: 'mov', channel2_task: 'or' };

        const result = generateTrialDirections(condition, trialAssignment);
        
        // Channel 1 movement task should be active
        expect([0, 180]).toContain(result.dir_mov_1);
        expect(result.dir_or_1).toBeNull();
        
        // Channel 2 orientation task should be active with same response dimension
        expect([0, 180]).toContain(result.dir_or_2);
        expect(result.dir_mov_2).toBeNull();
    });
});

describe('generateTaskAssignmentSequence', () => {
    test('should generate fixed assignment with 0% switch rate', () => {
        const result = generateTaskAssignmentSequence('mov', 'or', 4, 0);
        
        expect(result).toHaveLength(4);
        result.forEach(assignment => {
            expect(assignment.channel1_task).toBe('mov');
            expect(assignment.channel2_task).toBe('or');
        });
    });

    test('should generate alternating assignment with 100% switch rate', () => {
        const result = generateTaskAssignmentSequence('mov', 'or', 4, 100);
        
        expect(result).toHaveLength(4);
        expect(result[0].channel1_task).toBe('mov');
        expect(result[0].channel2_task).toBe('or');
        
        // With 100% switch rate, should alternate each trial
        expect(result[1].channel1_task).toBe('or');
        expect(result[1].channel2_task).toBe('mov');
        
        expect(result[2].channel1_task).toBe('mov');
        expect(result[2].channel2_task).toBe('or');
        
        expect(result[3].channel1_task).toBe('or');
        expect(result[3].channel2_task).toBe('mov');
    });

    test('should generate random assignment with 50% switch rate', () => {
        const result = generateTaskAssignmentSequence('mov', 'or', 10, 50);
        
        expect(result).toHaveLength(10);
        // First trial should always be default assignment
        expect(result[0].channel1_task).toBe('mov');
        expect(result[0].channel2_task).toBe('or');
        
        // With randomness, we can't predict exact sequence, but all assignments should be valid
        result.forEach(assignment => {
            expect(['mov', 'or']).toContain(assignment.channel1_task);
            expect(['mov', 'or']).toContain(assignment.channel2_task);
            expect(assignment.channel1_task).not.toBe(assignment.channel2_task);
        });
    });
});

describe('generateTaskSequence', () => {
    test('should generate AABB pattern correctly', () => {
        const result = generateTaskSequence('AABB', 8, 0);
        expect(result).toEqual(['mov', 'mov', 'or', 'or', 'mov', 'mov', 'or', 'or']);
    });

    test('should generate ABAB pattern correctly', () => {
        const result = generateTaskSequence('ABAB', 6, 0);
        expect(result).toEqual(['mov', 'or', 'mov', 'or', 'mov', 'or']);
    });

    test('should generate AAAABBBB pattern correctly', () => {
        const result = generateTaskSequence('AAAABBBB', 12, 0);
        expect(result).toEqual(['mov', 'mov', 'mov', 'mov', 'or', 'or', 'or', 'or', 'mov', 'mov', 'mov', 'mov']);
    });

    test('should generate Random sequence with correct length and valid tasks', () => {
        const result = generateTaskSequence('Random', 10, 50);
        
        expect(result).toHaveLength(10);
        result.forEach(task => {
            expect(['mov', 'or']).toContain(task);
        });
    });

    test('should generate alternating sequence for 100% switch rate', () => {
        const result = generateTaskSequence('Random', 6, 100);
        
        expect(result).toHaveLength(6);
        // With 100% switch rate, should alternate every trial
        for (let i = 1; i < result.length; i++) {
            expect(result[i]).not.toBe(result[i-1]);
        }
    });

    test('should generate same task sequence for 0% switch rate', () => {
        const result = generateTaskSequence('Random', 5, 0);
        
        expect(result).toHaveLength(5);
        // With 0% switch rate, all should be the same task
        const firstTask = result[0];
        result.forEach(task => {
            expect(task).toBe(firstTask);
        });
    });

    test('should default to alternating pattern for unknown sequence type', () => {
        const result = generateTaskSequence('UnknownType', 4, 0);
        expect(result).toEqual(['mov', 'or', 'mov', 'or']);
    });
});

describe('createTrialSequence', () => {
    test('Standard Dual-Task (Telford Condition)', () => {
        const condition = {
            Experiment: 'Telford',
            N_Tasks: 2,
            SOA: 100,
            Sequence_Type: 'Random',
            Switch_Rate_Percent: 0,
            Stimulus_Valency: 'Univalent',
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '0',   // Unused for dual-task
            effective_end_stim1_or: '0',     // Unused for dual-task
            effective_start_stim2_or: '200', // Channel 2 orientation task
            effective_end_stim2_or: '700',   // Channel 2 orientation task
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '150',
            effective_end_cue2: '200',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '200',
            effective_end_go2: '250',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        const trial = result[0];

        // Basic structure - correct dual-task assignment
        expect(trial.seParams.task_1).toBe('mov');
        expect(trial.seParams.task_2).toBe('or');

        // Channel 1: Movement task active
        expect(trial.seParams.dur_mov_1).toBeGreaterThan(0);
        expect(trial.seParams.dur_or_1).toBe(0);  // Channel 1 orientation unused

        // Channel 2: Orientation task active
        expect(trial.seParams.dur_or_2).toBeGreaterThan(0);
        expect(trial.seParams.dur_mov_2).toBe(0); // Channel 2 movement unused

        // Verify both channels have active cues
        expect(trial.seParams.dur_1).toBeGreaterThan(0);  // Channel 1 cue
        expect(trial.seParams.dur_2).toBeGreaterThan(0);  // Channel 2 cue
    });

    test('EXPECTED TO FAIL: Task-Switching (Jersild Condition)', () => {
        const condition = {
            Experiment: 'Jersild',
            N_Tasks: 1,
            SOA: 0,
            Sequence_Type: 'ABAB',
            Switch_Rate_Percent: 100,
            Stimulus_Valency: 'Univalent',
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '200',
            effective_end_stim1_or: '700',
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '0', // Single-task condition - cue2 should be inactive
            effective_end_cue2: '0',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '0', // Single-task condition - go2 should be inactive
            effective_end_go2: '0',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 2);
        const secondTrial = result[1]; // Should be 'or' trial

        // CRITICAL TEST THAT SHOULD FAIL: Second trial should have task_1 as 'or'
        expect(secondTrial.seParams.task_1).toBe('or');
        
        // task_2 should now be null due to our fix (single-task condition)
        expect(secondTrial.seParams.task_2).toBeNull();

        // Only the active task cue should be present
        expect(secondTrial.seParams.dur_1).toBeGreaterThan(0); // Active task cue
        expect(secondTrial.seParams.dur_2).toBe(0); // Inactive cue for single-task
    });

    test('Single Task with Distractor (Stroop/Flanker)', () => {
        const condition = {
            Experiment: 'Stroop',
            N_Tasks: 1,
            SOA: 0,
            Sequence_Type: 'Random',
            Switch_Rate_Percent: 0,
            Stimulus_Valency: 'Bivalent-Incongruent',
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '100', // Same start time for bivalent stimulus
            effective_end_stim1_or: '600',
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '0', // Inactive cue
            effective_end_cue2: '0',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '0',
            effective_end_go2: '0',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        const trial = result[0];

        // Should have one primary task (task_2 should now be null due to our fix)
        expect(trial.seParams.task_1).toBe('mov');
        expect(trial.seParams.task_2).toBeNull();

        // Both stimulus pathways should be active for bivalent stimulus
        expect(trial.seParams.dur_mov_1).toBeGreaterThan(0);
        expect(trial.seParams.dur_or_1).toBeGreaterThan(0);

        // Only task_1 cue should be active
        expect(trial.seParams.dur_1).toBeGreaterThan(0);
        expect(trial.seParams.dur_2).toBe(0);
    });

    test('Pre-cued Trial (Meiran)', () => {
        const csi = 500; // Cue-Stimulus Interval
        const condition = {
            Experiment: 'Meiran',
            N_Tasks: 1,
            CSI: csi,
            Sequence_Type: 'ABAB',
            Switch_Rate_Percent: 50,
            Stimulus_Valency: 'Univalent',
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: String(100 + csi), // Stimulus starts CSI ms after cue
            effective_end_stim1_mov: String(600 + csi),
            effective_start_stim1_or: String(100 + csi),
            effective_end_stim1_or: String(600 + csi),
            effective_start_cue1: '100',
            effective_end_cue1: '150',
            effective_start_cue2: '100',
            effective_end_cue2: '150',
            effective_start_go1: String(100 + csi),
            effective_end_go1: String(150 + csi),
            effective_start_go2: String(100 + csi),
            effective_end_go2: String(150 + csi),
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        const trial = result[0];

        // Test that stimulus starts exactly CSI ms after cue
        const cueStart = trial.seParams.start_1;
        const stimStart = trial.seParams.start_mov_1;
        
        expect(stimStart).toBe(cueStart + csi);
    });

    test('should generate correct number of trials', () => {
        const condition = {
            Experiment: 'Test',
            Sequence_Type: 'Random',
            Switch_Rate_Percent: 50,
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '200',
            effective_end_stim1_or: '700',
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '150',
            effective_end_cue2: '200',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '200',
            effective_end_go2: '250',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 5);
        expect(result).toHaveLength(5);
        
        result.forEach((trial, index) => {
            expect(trial.trialNumber).toBe(index + 1);
            expect(trial.seParams).toBeDefined();
            expect(trial.regenTime).toBeDefined();
            expect(trial.taskType).toMatch(/^(mov|or)$/);
        });
    });

    test('should include ITI in trial structure', () => {
        const condition = {
            Experiment: 'Test',
            ITI_ms: 1500,
            ITI_Distribution_Type: 'fixed',
            effective_start_stim1_mov: '100',
            effective_end_stim1_mov: '600',
            effective_start_stim1_or: '200',
            effective_end_stim1_or: '700',
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '150',
            effective_end_cue2: '200',
            effective_start_go1: '100',
            effective_end_go1: '150',
            effective_start_go2: '200',
            effective_end_go2: '250',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        expect(result[0].regenTime).toBe(1500);
    });
});

// NEW TEST CASES - These should initially FAIL, exposing current implementation flaws
describe('FAILING TESTS - N_Tasks Based Paradigm Differentiation', () => {
    
    test('SHOULD FAIL: Dual-Task (Hazeltine et al. 2006) - Disjoint Response Sets', () => {
        const condition = {
            Experiment: 'Hazeltine',
            N_Tasks: 2,
            Simplified_RSO: 'Disjoint', 
            Stimulus_Valency: 'Univalent',
            SOA: 0,
            Sequence_Type: 'Random',
            Switch_Rate_Percent: 0,
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            // Dual-task timing pattern
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '100',    // Both cues active
            effective_end_cue2: '150',      
            effective_start_go1: '200',
            effective_end_go1: '250', 
            effective_start_go2: '300',     // Both go signals active
            effective_end_go2: '350',
            // Task 1: Movement (Channel 1)
            effective_start_stim1_mov: '200',
            effective_end_stim1_mov: '700',
            effective_start_stim1_or: '0',  // Unused for dual-task
            effective_end_stim1_or: '0',
            // Task 2: Orientation (Channel 2) 
            effective_start_stim2_mov: '0', // Unused for dual-task
            effective_end_stim2_mov: '0',
            effective_start_stim2_or: '300', // Channel 2 orientation task
            effective_end_stim2_or: '800',   
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        const trial = result[0];

        // CRITICAL TEST: Should be dual-task with both channels active
        expect(trial.seParams.task_1).toBe('mov');
        expect(trial.seParams.task_2).toBe('or');
        
        // Channel 1: Movement task active
        expect(trial.seParams.dur_mov_1).toBeGreaterThan(0);
        expect(trial.seParams.dur_or_1).toBe(0);  // No distractor for univalent dual-task
        
        // Channel 2: Orientation task active  
        expect(trial.seParams.dur_or_2).toBeGreaterThan(0);  
        expect(trial.seParams.dur_mov_2).toBe(0); // No distractor for univalent dual-task
        
        // Direction assignments for disjoint response sets
        expect([0, 180]).toContain(trial.seParams.dir_mov_1);
        expect([90, 270]).toContain(trial.seParams.dir_or_2); // Orthogonal for disjoint
        
        // Both channels should have active cues and go signals
        expect(trial.seParams.dur_1).toBeGreaterThan(0);  // Channel 1 cue
        expect(trial.seParams.dur_2).toBeGreaterThan(0);  // Channel 2 cue
        expect(trial.seParams.dur_go_1).toBeGreaterThan(0); // Channel 1 go
        expect(trial.seParams.dur_go_2).toBeGreaterThan(0); // Channel 2 go
    });

    test('SHOULD FAIL: Task-Switching (Rogers & Monsell, 1995) - AABB Pattern', () => {
        const condition = {
            Experiment: 'Rogers_Monsell',
            N_Tasks: 1,
            Sequence_Type: 'AABB',
            Switch_Rate_Percent: 50,
            Stimulus_Valency: 'Univalent',
            Simplified_RSO: 'Identical',
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            // Single-task timing pattern - only Channel 1 active
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '0',      // Inactive for single-task
            effective_end_cue2: '0',        
            effective_start_go1: '200',
            effective_end_go1: '250',
            effective_start_go2: '0',       // Inactive for single-task
            effective_end_go2: '0',
            // Primary task stimuli (timing same for both mov and or)
            effective_start_stim1_mov: '200',
            effective_end_stim1_mov: '700',
            effective_start_stim1_or: '200',
            effective_end_stim1_or: '700',
            // Channel 2 completely inactive
            effective_start_stim2_mov: '0',
            effective_end_stim2_mov: '0',
            effective_start_stim2_or: '0',
            effective_end_stim2_or: '0',
            coh_1: '0.8',
            coh_2: '0.0'
        };

        const result = createTrialSequence(condition, 4);
        
        // AABB pattern: mov, mov, or, or
        expect(result[0].seParams.task_1).toBe('mov');
        expect(result[0].seParams.task_2).toBeNull();
        
        expect(result[1].seParams.task_1).toBe('mov'); 
        expect(result[1].seParams.task_2).toBeNull();
        
        expect(result[2].seParams.task_1).toBe('or');
        expect(result[2].seParams.task_2).toBeNull();
        
        expect(result[3].seParams.task_1).toBe('or');
        expect(result[3].seParams.task_2).toBeNull();
        
        // All trials should have only Channel 1 active
        result.forEach(trial => {
            expect(trial.seParams.dur_1).toBeGreaterThan(0);  // Channel 1 cue active
            expect(trial.seParams.dur_2).toBe(0);             // Channel 2 cue inactive
            expect(trial.seParams.dur_go_1).toBeGreaterThan(0); // Channel 1 go active
            expect(trial.seParams.dur_go_2).toBe(0);           // Channel 2 go inactive
        });
    });

    test('SHOULD FAIL: Single-Task with Asynchronous Distractor (Kopp et al. 1996)', () => {
        const condition = {
            Experiment: 'Kopp',
            N_Tasks: 1,
            SOA: -100,  // Distractor appears 100ms before target
            Stimulus_Valency: 'Bivalent-Incongruent',
            Simplified_RSO: 'Identical',
            Sequence_Type: 'Random',
            Switch_Rate_Percent: 0,
            ITI_ms: 1000,
            ITI_Distribution_Type: 'fixed',
            // Single-task with bivalent stimulus
            effective_start_cue1: '0',
            effective_end_cue1: '50',
            effective_start_cue2: '0',      // Inactive
            effective_end_cue2: '0',        
            effective_start_go1: '200',
            effective_end_go1: '250',
            effective_start_go2: '0',       // Inactive
            effective_end_go2: '0',
            // Target: movement task
            effective_start_stim1_mov: '200',
            effective_end_stim1_mov: '700', 
            // Distractor: orientation (earlier onset due to negative SOA)
            effective_start_stim1_or: '100',  // 100ms before target
            effective_end_stim1_or: '600',
            // Channel 2 inactive
            effective_start_stim2_mov: '0',
            effective_end_stim2_mov: '0',
            effective_start_stim2_or: '0',
            effective_end_stim2_or: '0',
            coh_1: '0.8',
            coh_2: '0.6'
        };

        const result = createTrialSequence(condition, 1);
        const trial = result[0];

        // Should be single-task with task_1 = 'mov', task_2 = null
        expect(trial.seParams.task_1).toBe('mov');
        expect(trial.seParams.task_2).toBeNull();
        
        // Both pathways of Channel 1 should be active (bivalent stimulus)
        expect(trial.seParams.dur_mov_1).toBeGreaterThan(0);  // Target
        expect(trial.seParams.dur_or_1).toBeGreaterThan(0);   // Distractor
        
        // Distractor should start 100ms before target (negative SOA)
        expect(trial.seParams.start_or_1).toBe(trial.seParams.start_mov_1 - 100);
        
        // Channel 2 should be completely inactive
        expect(trial.seParams.dur_2).toBe(0);
        expect(trial.seParams.dur_go_2).toBe(0);
        expect(trial.seParams.dur_mov_2).toBe(0);
        expect(trial.seParams.dur_or_2).toBe(0);
        
        // For incongruent condition, directions should be opposite
        if (trial.seParams.dir_mov_1 === 0) {
            expect(trial.seParams.dir_or_1).toBe(180);
        } else {
            expect(trial.seParams.dir_or_1).toBe(0);
        }
    });
});
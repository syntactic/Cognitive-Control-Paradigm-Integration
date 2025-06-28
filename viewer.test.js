// viewer.test.js

const { 
    generateITI, 
    convertAbsoluteToSEParams, 
    generateTrialDirections, 
    generateTaskSequence, 
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
    test('should generate congruent directions for Bivalent-Congruent condition', () => {
        const condition = {
            Stimulus_Valency: 'Bivalent-Congruent',
            Simplified_RSO: 'Identical'
        };

        // Run multiple times to test randomness and consistency
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition);
            
            // Both directions should be the same for congruent condition
            expect(result.mov_dir).toBe(result.or_dir);
            expect([0, 180]).toContain(result.mov_dir);
            expect([0, 180]).toContain(result.or_dir);
        }
    });

    test('should generate incongruent directions for Bivalent-Incongruent condition', () => {
        const condition = {
            Stimulus_Valency: 'Bivalent-Incongruent',
            Simplified_RSO: 'Identical'
        };

        // Run multiple times to test randomness and consistency
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition);
            
            // Directions should be opposite for incongruent condition
            expect(result.mov_dir).not.toBe(result.or_dir);
            expect([0, 180]).toContain(result.mov_dir);
            expect([0, 180]).toContain(result.or_dir);
            
            // Specifically test opposition
            if (result.mov_dir === 0) {
                expect(result.or_dir).toBe(180);
            } else {
                expect(result.or_dir).toBe(0);
            }
        }
    });

    test('should generate orthogonal directions for Bivalent-Neutral condition', () => {
        const condition = {
            Stimulus_Valency: 'Bivalent-Neutral',
            Simplified_RSO: 'Identical'
        };

        // Run multiple times to test randomness
        for (let i = 0; i < 10; i++) {
            const result = generateTrialDirections(condition);
            
            // Movement should be horizontal (0 or 180)
            expect([0, 180]).toContain(result.mov_dir);
            // Orientation should be vertical (90 or 270)
            expect([90, 270]).toContain(result.or_dir);
        }
    });

    test('should generate random directions for Univalent condition', () => {
        const condition = {
            Stimulus_Valency: 'Univalent',
            Simplified_RSO: 'Identical'
        };

        const result = generateTrialDirections(condition);
        
        expect([0, 180]).toContain(result.mov_dir);
        expect([0, 180]).toContain(result.or_dir);
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
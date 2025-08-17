// viewer.test.js

const { 
    generateITI, 
    convertAbsoluteToSEParams, 
    generateTrialDirections, 
    generateTaskSequence, 
    generateTaskAssignmentSequence,
    createTrialSequence,
    updateInfoPanel,
    updateInfoPanelFromCondition,
    parseCSV,
    groupByBlock,
    generateDynamicSOA,
    recalculateTimingsWithDynamicSOA,
    extractMappingNotes
} = require('./viewer.js');

// Import test fixtures
const {
    multiConditionBlock,
    singleConditionBlock,
    dynamicDistributionBlock,
    dualTaskConditionForRelativeTiming,
    inconsistentConfigBlock
} = require('./viewer.test.data.js');

describe('generateITI', () => {
    test('should return the fixed RSI value when the distribution type is "fixed"', () => {
        const condition = {
            RSI_Distribution_Type: 'fixed',
            ITI_ms: '1200'
        };
        expect(generateITI(condition)).toBe(1200);
    });

    test('should return a value within the specified range for a "uniform" distribution', () => {
        const condition = {
            RSI_Distribution_Type: 'uniform',
            RSI_Distribution_Params: '[500, 600]'
        };
        const result = generateITI(condition);
        expect(result).toBeGreaterThanOrEqual(500);
        expect(result).toBeLessThanOrEqual(600);
    });

    test('should return a value from the choice array for "choice" distribution', () => {
        const condition = {
            RSI_Distribution_Type: 'choice',
            RSI_Distribution_Params: '[800, 1000, 1200]'
        };
        const result = generateITI(condition);
        expect([800, 1000, 1200]).toContain(result);
    });

    test('should gracefully fall back to default when ITI_ms is not a number', () => {
        const condition = {
            RSI_Distribution_Type: 'fixed',
            ITI_ms: 'invalid'
        };
        const result = generateITI(condition);
        expect(result).toBe(1000); // Default fallback
    });

    test('should gracefully fall back to base ITI when RSI_Distribution_Params is invalid JSON', () => {
        const condition = {
            RSI_Distribution_Type: 'uniform',
            ITI_ms: '1500',
            RSI_Distribution_Params: 'invalid json'
        };
        const result = generateITI(condition);
        expect(result).toBe(1500); // Falls back to base ITI
    });

    test('should default to 1000ms when no ITI_ms is provided', () => {
        const condition = {
            RSI_Distribution_Type: 'fixed'
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

    test('should correctly calculate Task 2 relative timings for SE package', () => {
        // This test verifies the CRITICAL relative timing calculations
        // Based on trial.js, Task 2 timings are relative to Task 1 end times
        const result = convertAbsoluteToSEParams(dualTaskConditionForRelativeTiming);

        // From dualTaskConditionForRelativeTiming:
        // Task 1 Movement (Channel 1): starts at 100ms, ends at 600ms
        // Task 2 Orientation (Channel 2): starts at 200ms, ends at 700ms
        
        // Basic dual-task structure
        expect(result.task_1).toBe('mov');
        expect(result.task_2).toBe('or');
        
        // Task 1 timings should remain absolute
        expect(result.start_mov_1).toBe(100);
        expect(result.dur_mov_1).toBe(500); // 600 - 100
        
        // Task 2 timings should be RELATIVE to Task 1 end times
        // start_mov_2 should be: start_stim2_mov - end_stim1_mov
        // Since stim2_mov is not active (start=0, end=0), this should be 0
        expect(result.start_mov_2).toBe(0);
        expect(result.dur_mov_2).toBe(0);
        
        // start_or_2 should be: start_stim2_or - end_stim1_or 
        // According to trial.js: or2Interval.addTime(or1Interval.end)
        // From test data: stim1_or is inactive (0,0), stim2_or is (200,700)
        // So start_or_2 should be: 200 - 0 = 200
        // This means Channel 2 orientation starts 200ms after Channel 1 orientation ends
        expect(result.start_or_2).toBe(200); // Relative to Channel 1 orientation end (which is 0)
        expect(result.dur_or_2).toBe(500); // 700 - 200
        
        // Channel 1 orientation pathway should be inactive for univalent dual-task
        expect(result.start_or_1).toBe(0);
        expect(result.dur_or_1).toBe(0);
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

// NEW TEST CASES FOR BLOCK-AWARE FUNCTIONALITY
describe('generateSOA', () => {
    test('should return fixed SOA value for fixed distribution', () => {
        const condition = {
            SOA_Distribution_Type: 'fixed',
            SOA_Distribution_Params: '[]'
        };
        const baseSoa = 100;
        
        const { generateSOA } = require('./viewer.js');
        const result = generateSOA(condition, baseSoa);
        expect(result).toBe(100); // Should return base SOA for fixed distribution
    });

    test('should generate uniform distribution SOA values', () => {
        const condition = {
            SOA_Distribution_Type: 'uniform',
            SOA_Distribution_Params: '[50, 200]'
        };
        
        const { generateSOA } = require('./viewer.js');
        const result = generateSOA(condition, 100);
        expect(result).toBeGreaterThanOrEqual(50);
        expect(result).toBeLessThanOrEqual(200);
    });

    test('should generate choice distribution SOA values', () => {
        const condition = dynamicDistributionBlock[1]; // Uses choice distribution
        
        const { generateSOA } = require('./viewer.js');
        const result = generateSOA(condition, 100);
        expect([0, 100, 200]).toContain(result);
    });
});

describe('Block Grouping Logic', () => {
    test('should group conditions by Block_ID', () => {
        const testData = [
            ...multiConditionBlock,
            ...singleConditionBlock
        ];
        
        const { groupByBlock } = require('./viewer.js');
        const groups = groupByBlock(testData);
        
        expect(groups['TestBlock_A']).toHaveLength(3);
        expect(groups['SingleCondition_Test']).toHaveLength(1); // Uses Experiment name as fallback
    });
});

describe('Block-Aware Trial Generation', () => {
    test('should prioritize Sequence_Type from viewer_config over Switch_Rate_Percent', () => {
        // Test using the full multi-condition block with AABB sequence type in viewer_config
        const result = createTrialSequence(multiConditionBlock, 4);
        
        // Should generate 4 trials following AABB pattern
        expect(result).toHaveLength(4);
        expect(result[0].taskType).toBe('mov');  // First A
        expect(result[1].taskType).toBe('mov');  // Second A
        expect(result[2].taskType).toBe('or');   // First B
        expect(result[3].taskType).toBe('or');   // Second B
        
        // Verify trials have the correct transition types
        expect(result[0].transitionType).toBe('Pure');   // First trial is always pure
        expect(result[1].transitionType).toBe('Repeat'); // Second A is repeat
        expect(result[2].transitionType).toBe('Switch'); // First B is switch
        expect(result[3].transitionType).toBe('Repeat'); // Second B is repeat
    });

    test('should map trials to correct condition rows based on Trial_Transition_Type', () => {
        const result = createTrialSequence(multiConditionBlock, 4);
        
        // First trial (Pure) should find the matching Pure condition
        const firstTrial = result[0];
        expect(firstTrial.transitionType).toBe('Pure');
        expect(firstTrial.selectedCondition).toBe('TestBlock_A_Pure'); // Finds matching Pure condition
        expect(firstTrial.seParams.coh_1).toBe(0.9); // From Pure condition
        
        // Second trial (Repeat) should use the Repeat condition
        const secondTrial = result[1];
        expect(secondTrial.transitionType).toBe('Repeat');
        expect(secondTrial.selectedCondition).toBe('TestBlock_A_Repeat');
        expect(secondTrial.seParams.coh_1).toBe(0.6); // From Repeat condition, not Switch
        
        // Third trial (Switch) should use the Switch condition
        const thirdTrial = result[2];
        expect(thirdTrial.transitionType).toBe('Switch');
        expect(thirdTrial.selectedCondition).toBe('TestBlock_A_Switch');
        expect(thirdTrial.seParams.coh_1).toBe(0.8); // From Switch condition
        
        // Fourth trial (Repeat) should use the Repeat condition again
        const fourthTrial = result[3];
        expect(fourthTrial.transitionType).toBe('Repeat');
        expect(fourthTrial.selectedCondition).toBe('TestBlock_A_Repeat');
        expect(fourthTrial.seParams.coh_1).toBe(0.6); // From Repeat condition
    });

    test('should handle dynamic SOA generation per trial', () => {
        const condition = dynamicDistributionBlock[0]; // Uniform SOA distribution
        
        const result = createTrialSequence(condition, 2);
        
        // Each trial should include dynamic SOA values
        expect(result).toHaveLength(2);
        expect(result[0].dynamicSOA).toBeGreaterThanOrEqual(50);
        expect(result[0].dynamicSOA).toBeLessThanOrEqual(200);
        expect(result[1].dynamicSOA).toBeGreaterThanOrEqual(50);
        expect(result[1].dynamicSOA).toBeLessThanOrEqual(200);
    });

    test('should handle dynamic RSI generation per trial', () => {
        const condition = dynamicDistributionBlock[1]; // Choice RSI distribution
        
        const result = createTrialSequence(condition, 3);
        
        // Each trial should get RSI from the choice array (now works with RSI columns)
        const rsiValues = result.map(trial => trial.regenTime);
        rsiValues.forEach(rsi => {
            expect([500, 1000, 1500, 2000]).toContain(rsi);
        });
    });

    test('should work with single conditions (backward compatibility)', () => {
        // Test that the function still works with single conditions
        const singleCondition = multiConditionBlock[0];
        const result = createTrialSequence(singleCondition, 3);
        
        expect(result).toHaveLength(3);
        expect(result[0].seParams.coh_1).toBe(0.8); // Uses single condition parameters
        expect(result[0].selectedCondition).toBe('TestBlock_A_Switch');
    });

    test('should handle inconsistent viewer_config gracefully (primary condition rule)', () => {
        // Test that viewer gracefully uses primary condition config when inconsistencies exist
        const result = createTrialSequence(inconsistentConfigBlock, 4);
        
        // Should complete successfully without throwing errors
        expect(result).toHaveLength(4);
        
        // Should use AABB pattern from primary condition, not ABAB from secondary
        expect(result[0].taskType).toBe('mov');  // First A
        expect(result[1].taskType).toBe('mov');  // Second A  
        expect(result[2].taskType).toBe('or');   // First B
        expect(result[3].taskType).toBe('or');   // Second B
        
        // Should use parameters from appropriate conditions based on transition type
        expect(result[0].seParams.coh_1).toBe(0.8); // From primary (Switch) condition
        expect(result[1].seParams.coh_1).toBe(0.6); // From Repeat condition
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

// NEW TESTS FOR BUG FIXES AND ENHANCEMENTS
describe('updateInfoPanel', () => {
    beforeEach(() => {
        // Set up DOM
        document.body.innerHTML = '<div id="info-panel"></div>';
    });
    
    test('should handle missing conceptual row gracefully', () => {
        updateInfoPanel(null);
        const infoPanel = document.getElementById('info-panel');
        expect(infoPanel.innerHTML).toContain('Experiment data not found');
    });
    
    test('should correctly map column names with fallbacks', () => {
        const conceptualRow = {
            'Experiment': 'Test Experiment',
            'Number of Tasks': '2',
            'Inter-task SOA': '100',
            'Task 1 Type': 'Color Discrimination',
            'Task 2 Type': 'Shape Discrimination',
            'Task 1 Stimulus-Response Mapping': 'Compatible',
            'Task 2 Stimulus-Response Mapping': 'Arbitrary',
            'Stimulus Valency': 'Bivalent-Congruent',
            'Response Set Overlap': 'Identical',
            'Switch Rate': '50',
            'Notes': 'Test notes'
        };
        
        updateInfoPanel(conceptualRow);
        const infoPanel = document.getElementById('info-panel');
        const content = infoPanel.innerHTML;
        
        expect(content).toContain('Test Experiment');
        expect(content).toContain('Number of Tasks:</strong> 2');
        expect(content).toContain('SOA:</strong> 100ms');
        expect(content).toContain('Task 1 SRM:</strong> Compatible');
        expect(content).toContain('Task 2 SRM:</strong> Arbitrary');
        expect(content).toContain('Switch Rate:</strong> 50%');
    });
    
    test('should handle single task experiments correctly', () => {
        const conceptualRow = {
            'Experiment': 'Single Task Test',
            'Number of Tasks': '1',
            'Task 1 Type': 'Arrow Identification',
            'Task 1 Stimulus-Response Mapping': 'Compatible',
            'Stimulus Valency': 'Univalent'
        };
        
        updateInfoPanel(conceptualRow);
        const infoPanel = document.getElementById('info-panel');
        const content = infoPanel.innerHTML;
        
        expect(content).toContain('Number of Tasks:</strong> 1');
        expect(content).toContain('Stimulus Response Mapping:</strong> Compatible');
        expect(content).not.toContain('Task 2 Type');
        expect(content).not.toContain('Task 2 SRM');
    });
});

describe('updateInfoPanelFromCondition', () => {
    beforeEach(() => {
        document.body.innerHTML = '<div id="info-panel"></div>';
    });
    
    test('should handle missing condition gracefully', () => {
        updateInfoPanelFromCondition(null);
        const infoPanel = document.getElementById('info-panel');
        expect(infoPanel.innerHTML).toContain('Condition data not found');
    });
    
    test('should correctly display dual-task condition data', () => {
        const condition = {
            'Experiment': 'Dual Task Test',
            'N_Tasks': 2,
            'Task_1_Type': 'Movement',
            'Task_2_Type': 'Orientation',
            'SRM_1': 'Compatible',
            'SRM_2': 'Arbitrary',
            'Stimulus_Valency': 'Univalent',
            'Simplified_RSO': 'Disjoint',
            'Sequence_Type': 'Random',
            'Switch_Rate_Percent': '25',
            'ITI_ms': '1500',
            'RSI_Distribution_Type': 'uniform'
        };
        
        updateInfoPanelFromCondition(condition);
        const infoPanel = document.getElementById('info-panel');
        const content = infoPanel.innerHTML;
        
        expect(content).toContain('Dual Task Test');
        expect(content).toContain('Number of Tasks:</strong> 2');
        expect(content).toContain('Task 1 SRM:</strong> Compatible');
        expect(content).toContain('Task 2 SRM:</strong> Arbitrary');
        expect(content).toContain('Switch Rate:</strong> 25%');
        expect(content).toContain('ITI:</strong> 1500ms (uniform)');
    });
});

// REGRESSION TESTS for previously identified issues
describe('Regression Tests', () => {
    test('should not display undefined in SOA field', () => {
        document.body.innerHTML = '<div id="info-panel"></div>';
        
        const conceptualRow = {
            'Experiment': 'Test',
            'Number of Tasks': '1',
            'SOA': undefined, // This was causing "undefined" to appear
            'Inter-task SOA': null
        };
        
        updateInfoPanel(conceptualRow);
        const content = document.getElementById('info-panel').innerHTML;
        
        expect(content).not.toContain('undefinedms');
        expect(content).toContain('SOA:</strong> N/A');
    });
    
    test('should not display undefined in Stimulus Response Mapping field', () => {
        document.body.innerHTML = '<div id="info-panel"></div>';
        
        const conceptualRow = {
            'Experiment': 'Test',
            'Number of Tasks': '1',
            'Stimulus Response Mapping': undefined, // This was causing issues
            'Task 1 Stimulus-Response Mapping': 'Compatible'
        };
        
        updateInfoPanel(conceptualRow);
        const content = document.getElementById('info-panel').innerHTML;
        
        expect(content).not.toContain('Stimulus Response Mapping:</strong> undefined');
        expect(content).toContain('Stimulus Response Mapping:</strong> Compatible');
    });
});

// NEW TESTS FOR DYNAMIC SOA FUNCTIONALITY
describe('Dynamic SOA Generation', () => {
    test('should extract SOA distribution from mapping notes', () => {
        const condition = {
            'Super_Experiment_Mapping_Notes': '{"viewer_config": {"SOA_distribution": "choice", "SOA_values": [1000, 2000, 4000, 8000, 16000]}}'
        };
        
        const notes = extractMappingNotes(condition);
        expect(notes.viewer_config.SOA_distribution).toBe('choice');
        expect(notes.viewer_config.SOA_values).toEqual([1000, 2000, 4000, 8000, 16000]);
    });
    
    test('should generate SOA from discrete choice distribution', () => {
        const condition = {
            'Super_Experiment_Mapping_Notes': '{"viewer_config": {"SOA_distribution": "choice", "SOA_values": [1000, 2000, 4000, 8000, 16000]}}'
        };
        
        // Test multiple samples to ensure they're all from the valid set
        for (let i = 0; i < 10; i++) {
            const soa = generateDynamicSOA(condition);
            expect([1000, 2000, 4000, 8000, 16000]).toContain(soa);
        }
    });
    
    test('should generate SOA from uniform distribution', () => {
        const condition = {
            'Super_Experiment_Mapping_Notes': '{"viewer_config": {"SOA_distribution": "uniform", "SOA_range": [500, 1500]}}'
        };
        
        const soa = generateDynamicSOA(condition);
        expect(soa).toBeGreaterThanOrEqual(500);
        expect(soa).toBeLessThanOrEqual(1500);
    });
    
    test('should fallback to generateSOA when no viewer config', () => {
        const condition = {
            'SOA_Distribution_Type': 'fixed'
        };
        
        const soa = generateDynamicSOA(condition);
        expect(soa).toBe(0); // Default from generateSOA
    });
});

describe('Timing Recalculation', () => {
    test('should recalculate T2 timings based on dynamic SOA', () => {
        const condition = {
            'N_Tasks': '2',
            'Inter-task SOA': '6200', // Original static SOA
            'effective_start_stim1_mov': '100',
            'effective_start_stim2_or': '6300', // Original T2 timing
            'effective_end_stim2_or': '8300',
            'effective_start_cue2': '4300',
            'effective_end_cue2': '6300',
            'Task 2 CSI': '2000'
        };
        
        const dynamicSOA = 4000; // New SOA
        const result = recalculateTimingsWithDynamicSOA(condition, dynamicSOA);
        
        // T2 stimulus should start at T1_start + dynamic_SOA = 100 + 4000 = 4100
        expect(parseInt(result.effective_start_stim2_or)).toBe(4100);
        expect(parseInt(result.effective_end_stim2_or)).toBe(6100); // 4100 + 2000 duration
        
        // T2 cue should start CSI ms before T2 stimulus = 4100 - 2000 = 2100
        expect(parseInt(result.effective_start_cue2)).toBe(2100);
    });
    
    test('should handle single-task experiments without modification', () => {
        const condition = {
            'N_Tasks': '1',
            'effective_start_stim1_mov': '100',
            'effective_end_stim1_mov': '600'
        };
        
        const dynamicSOA = 2000;
        const result = recalculateTimingsWithDynamicSOA(condition, dynamicSOA);
        
        // Should return unchanged condition for single-task
        expect(result.effective_start_stim1_mov).toBe('100');
        expect(result.effective_end_stim1_mov).toBe('600');
    });
    
    test('should handle invalid JSON in mapping notes gracefully', () => {
        const condition = {
            'Super_Experiment_Mapping_Notes': 'invalid json'
        };
        
        expect(() => extractMappingNotes(condition)).not.toThrow();
        expect(() => generateDynamicSOA(condition)).not.toThrow();
    });
});
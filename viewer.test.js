// viewer.test.js

const { generateITI } = require('./viewer.js');

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
});

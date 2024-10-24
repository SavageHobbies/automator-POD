// frontend/src/components/DesignWorkflow/index.js
import React, { useState } from 'react';
import ApiService from '../../services/api';

function DesignWorkflow() {
    const [prompt, setPrompt] = useState('');
    const [design, setDesign] = useState(null);
    const [mockups, setMockups] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = async () => {
        setIsLoading(true);
        try {
            // Generate design
            const designResult = await ApiService.generateDesign(prompt);
            setDesign(designResult.design);

            // Generate mockups
            const mockupsResult = await ApiService.generateMockups(designResult.design);
            setMockups(mockupsResult.mockups);
        } catch (error) {
            console.error('Generation failed:', error);
        }
        setIsLoading(false);
    };

    const handlePublish = async () => {
        setIsLoading(true);
        try {
            const result = await ApiService.publishProduct(design, mockups);
            if (result.success) {
                alert('Product published successfully!');
            }
        } catch (error) {
            console.error('Publishing failed:', error);
        }
        setIsLoading(false);
    };

    return (
        <div className="design-workflow">
            <input
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your design idea..."
            />
            <button onClick={handleGenerate} disabled={isLoading}>
                Generate Design
            </button>

            {design && (
                <div className="design-preview">
                    <h3>Generated Design</h3>
                    {/* Design preview component */}
                </div>
            )}

            {mockups.length > 0 && (
                <div className="mockups-preview">
                    <h3>Generated Mockups</h3>
                    {/* Mockups preview component */}
                    <button onClick={handlePublish} disabled={isLoading}>
                        Publish to Printify
                    </button>
                </div>
            )}
        </div>
    );
}

export default DesignWorkflow;
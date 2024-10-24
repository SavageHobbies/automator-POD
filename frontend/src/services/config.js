const config = {
    apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    endpoints: {
        design: '/api/designs',
        mockup: '/api/mockups',
        publish: '/api/designs/publish'
    },
    dynamicMockups: {
        apiKey: process.env.REACT_APP_DYNAMIC_MOCKUPS_API_KEY,
        baseUrl: 'https://api.dynamicmockups.com/v1'
    }
};

export default config;
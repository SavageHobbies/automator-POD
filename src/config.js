// Configuration for the application
const config = {
    // API endpoint - change this to match your backend server
    API_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',

    // S3 bucket for storing generated mockups
    S3_BUCKET: process.env.REACT_APP_S3_BUCKET || 'max-pod-designs',

    // Categories available for mockup generation
    MOCKUP_CATEGORIES: [
        'blankets', 'hoodies', 'mugs', 'ornaments', 'phone', 'pillows',
        'puzzles', 'sweatshirts', 'totes', 'tshirt', 'tumblers'
    ]
};

export default config;
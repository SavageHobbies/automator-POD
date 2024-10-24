// frontend/src/services/api.js
import axios from 'axios';
import config from './config';

const api = axios.create({
    baseURL: config.apiUrl
});

const dynamicMockupsApi = axios.create({
    baseURL: config.dynamicMockups.baseUrl,
    headers: {
        'Authorization': `Bearer ${config.dynamicMockups.apiKey}`,
        'Content-Type': 'application/json'
    }
});

class ApiService {
    async generateDesign(prompt) {
        const response = await api.post('/api/designs/generate', { prompt });
        return response.data;
    }

    async generateMockups(designData) {
        // First generate mockup using Dynamic Mockups API
        const mockupResponse = await dynamicMockupsApi.post('/mockups/generate', {
            template: 'product',
            design: designData.imageUrl
        });

        // Then store mockup data in our backend
        const response = await api.post('/api/mockups/generate', {
            designData,
            mockupData: mockupResponse.data
        });
        return response.data;
    }

    async publishProduct(designData, mockupPaths) {
        const response = await api.post('/api/designs/publish', {
            designData,
            mockupPaths
        });
        return response.data;
    }

    async getMockupTemplates() {
        const response = await dynamicMockupsApi.get('/templates');
        return response.data;
    }
}

export default new ApiService();
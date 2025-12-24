/**
 * Configuração da Aplicação PetStory
 * Este arquivo contém as configurações da API e ambiente
 * Pode ser substituído durante o deploy para diferentes ambientes
 */
window.APP_CONFIG = {
    // URL da API em produção
    API_URL: 'https://petstory.finderbit.com.br',
    
    // Ambiente atual (development, staging, production)
    ENVIRONMENT: 'production',
    
    // URLs do site (para meta tags e links)
    SITE_URL: window.location.origin,
    
    // Configurações de debug
    DEBUG: false
};

// Fallback para desenvolvimento local
if (window.location.hostname === 'localhost' || 
    window.location.hostname === '127.0.0.1' ||
    window.location.protocol === 'file:') {
    window.APP_CONFIG.API_URL = 'http://localhost:8000';
    window.APP_CONFIG.ENVIRONMENT = 'development';
    window.APP_CONFIG.DEBUG = true;
}

console.log('🔧 Configuração carregada:', window.APP_CONFIG);


// Sistema de tradução
class Translator {
    constructor() {
        this.currentLang = localStorage.getItem('language') || 'pt';
        this.init();
    }

    init() {
        // Carregar idioma salvo
        this.setLanguage(this.currentLang);
        
        // Adicionar event listeners aos botões de idioma
        document.querySelectorAll('.language-switcher').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const lang = e.currentTarget.dataset.lang;
                this.setLanguage(lang);
            });
        });
    }

    setLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem('language', lang);
        
        // Atualizar atributo lang do HTML
        document.documentElement.lang = lang;
        
        // Atualizar título da página
        const titleKey = document.querySelector('[data-translate="title"]');
        if (titleKey) {
            document.title = this.translate('title');
        }
        
        // Traduzir todos os elementos com data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            let translation = this.translate(key);
            
            // Se o elemento tem placeholders, substituir
            if (element.hasAttribute('data-translate-params')) {
                try {
                    const params = JSON.parse(element.getAttribute('data-translate-params'));
                    translation = this.translateWithParams(key, params);
                } catch (e) {
                    // Se falhar ao parsear JSON, usar tradução simples
                    console.warn('Erro ao parsear parâmetros de tradução:', e);
                }
            }
            
            // Verificar se é placeholder
            if (element.tagName === 'INPUT' && element.type !== 'submit' && element.type !== 'button') {
                element.placeholder = translation;
            } else if (element.tagName === 'BUTTON' || element.type === 'submit') {
                // Preservar ícones dentro do botão
                const icon = element.querySelector('i');
                if (icon) {
                    element.innerHTML = icon.outerHTML + ' ' + translation;
                } else {
                    element.textContent = translation;
                }
            } else {
                // Para outros elementos, verificar se há ícones ou outros elementos filhos
                const children = Array.from(element.children);
                const hasIcons = children.some(child => child.tagName === 'I' || child.tagName === 'SPAN');
                
                if (hasIcons) {
                    // Preservar elementos filhos e adicionar tradução
                    const existingContent = Array.from(element.childNodes).filter(node => 
                        node.nodeType === 1 && (node.tagName === 'I' || node.tagName === 'SPAN')
                    );
                    if (existingContent.length > 0) {
                        const existingHTML = existingContent.map(node => node.outerHTML).join(' ');
                        element.innerHTML = existingHTML + ' ' + translation;
                    } else {
                        element.textContent = translation;
                    }
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        // Atualizar botões de idioma
        document.querySelectorAll('.language-switcher').forEach(btn => {
            if (btn.dataset.lang === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Traduzir textos dinâmicos de pontos turísticos
        this.translateDynamicContent();
    }
    
    translateDynamicContent() {
        // Traduzir textos "Gratuito" e "Não informado" em inputs e spans
        document.querySelectorAll('.dynamic-translate').forEach(element => {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                const value = element.value.trim();
                if (value) {
                    const translated = this.translateDynamicText(value);
                    if (translated !== value) {
                        element.value = translated;
                    }
                }
            } else {
                const text = element.textContent.trim();
                const translated = this.translateDynamicText(text);
                if (translated !== text) {
                    element.textContent = translated;
                }
            }
        });
        
        // Traduzir textos de avaliações
        document.querySelectorAll('.total-avaliacoes').forEach(element => {
            const text = element.textContent.trim();
            const translated = this.translateDynamicText(text);
            if (translated !== text) {
                element.textContent = translated;
            }
        });
        
        // Traduzir descrições usando tradução básica de palavras comuns
        if (this.currentLang === 'en') {
            document.querySelectorAll('.dynamic-translate-desc').forEach(element => {
                let text = element.textContent;
                
                // Dicionário básico de traduções comuns para descrições turísticas
                const commonTranslations = {
                    'localizado': 'located',
                    'Localizado': 'Located',
                    'situado': 'situated',
                    'Situado': 'Situated',
                    'conhecido': 'known',
                    'Conhecido': 'Known',
                    'famoso': 'famous',
                    'Famoso': 'Famous',
                    'histórico': 'historical',
                    'Histórico': 'Historical',
                    'turístico': 'tourist',
                    'Turístico': 'Tourist',
                    'ponto turístico': 'tourist attraction',
                    'Ponto turístico': 'Tourist attraction',
                    'atração': 'attraction',
                    'Atração': 'Attraction',
                    'visitar': 'visit',
                    'Visitar': 'Visit',
                    'conhecer': 'get to know',
                    'Conhecer': 'Get to know',
                    'apreciar': 'appreciate',
                    'Apreciar': 'Appreciate',
                    'desfrutar': 'enjoy',
                    'Desfrutar': 'Enjoy',
                    'horário': 'hours',
                    'Horário': 'Hours',
                    'funcionamento': 'operation',
                    'Funcionamento': 'Operation',
                    'entrada': 'entrance',
                    'Entrada': 'Entrance',
                    'gratuito': 'free',
                    'Gratuito': 'Free',
                    'gratuita': 'free',
                    'Gratuita': 'Free',
                    'pago': 'paid',
                    'Pago': 'Paid',
                    'paga': 'paid',
                    'Paga': 'Paid'
                };
                
                // Aplicar traduções básicas
                Object.keys(commonTranslations).forEach(ptWord => {
                    const regex = new RegExp(ptWord, 'gi');
                    text = text.replace(regex, commonTranslations[ptWord]);
                });
                
                // Atualizar apenas se houver mudanças
                if (text !== element.textContent) {
                    element.textContent = text;
                }
            });
        }
    }

    translate(key) {
        if (translations[this.currentLang] && translations[this.currentLang][key]) {
            return translations[this.currentLang][key];
        }
        // Fallback para português se não encontrar a tradução
        if (translations['pt'] && translations['pt'][key]) {
            return translations['pt'][key];
        }
        return key; // Retornar a chave se não encontrar tradução
    }

    translateWithParams(key, params) {
        let translation = this.translate(key);
        Object.keys(params).forEach(param => {
            translation = translation.replace(`{${param}}`, params[param]);
        });
        return translation;
    }

    getCurrentLanguage() {
        return this.currentLang;
    }
    
    translateDynamicText(text) {
        if (!text) return text;
        
        const translations = {
            'Gratuito': this.currentLang === 'en' ? 'Free' : 'Gratuito',
            'Não informado': this.currentLang === 'en' ? 'Not informed' : 'Não informado',
            'Não informado.': this.currentLang === 'en' ? 'Not informed.' : 'Não informado.',
            'avaliações': this.currentLang === 'en' ? 'reviews' : 'avaliações',
            'avaliação': this.currentLang === 'en' ? 'review' : 'avaliação',
            '(0 avaliações)': this.currentLang === 'en' ? '(0 reviews)' : '(0 avaliações)',
            '(1 avaliação)': this.currentLang === 'en' ? '(1 review)' : '(1 avaliação)'
        };
        
        // Verificar tradução exata
        if (translations[text]) {
            return translations[text];
        }
        
        // Verificar padrões como "(X avaliações)"
        const avaliacoesPattern = /\((\d+)\s+avaliações?\)/;
        const match = text.match(avaliacoesPattern);
        if (match) {
            const count = match[1];
            const word = count === '1' ? 'review' : 'reviews';
            return this.currentLang === 'en' ? `(${count} ${word})` : text;
        }
        
        return text;
    }
}

// Inicializar tradutor quando o DOM estiver pronto
let translator;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        translator = new Translator();
    });
} else {
    translator = new Translator();
}


/* ========================================
   🎯 SCRIPTS E INTERATIVIDADES
   ======================================== */

/* Slider Comparativo - Versão Final Funcional */
(function() {
    var activeContainer = null;
    var activeSlider = null;
    
    function initComparisons() {
        var containers = document.querySelectorAll(".img-comp-container");
        
        if (containers.length === 0) {
            return;
        }
        
        containers.forEach(function(container, index) {
            if (container.dataset.sliderReady === 'true') {
                return;
            }
            
            var overlay = container.querySelector('.img-comp-overlay');
            if (!overlay) {
                return;
            }
            
            var overlayImg = overlay.querySelector('img');
            if (!overlayImg) {
                return;
            }
            
            var baseImgContainer = container.querySelector('.img-comp-img:not(.img-comp-overlay)');
            if (!baseImgContainer) {
                return;
            }
            var baseImg = baseImgContainer.querySelector('img');
            if (!baseImg) {
                return;
            }
            
            // Espera container e imagens carregarem
            function setup() {
                var w = container.offsetWidth;
                var rect = container.getBoundingClientRect();
                
                // Usa getBoundingClientRect que é mais confiável
                if (rect.width > 0) {
                    w = rect.width;
                }
                
                if (w === 0 || w < 10) {
                    setTimeout(setup, 300);
                    return;
                }
                
                container.dataset.sliderReady = 'true';
                
                // Configura overlay
                overlay.style.width = (w / 2) + "px";
                overlayImg.style.width = w + "px";
                overlayImg.style.height = "100%";
                
                // Cria slider se não existir
                var slider = container.querySelector('.img-comp-slider');
                if (!slider) {
                    slider = document.createElement("div");
                    slider.className = "img-comp-slider";
                    slider.innerHTML = "<i class='fas fa-arrows-alt-h text-gray-800' aria-label='Arraste para comparar antes e depois'></i>";
                    container.appendChild(slider);
                }
                
                // Cria divider se não existir
                var divider = container.querySelector('.img-comp-divider');
                if (!divider) {
                    divider = document.createElement("div");
                    divider.className = "img-comp-divider";
                    container.appendChild(divider);
                }
                
                // Função para atualizar posição
                function moveSlider(x) {
                    x = Math.max(0, Math.min(container.offsetWidth, x));
                    overlay.style.width = x + "px";
                    if (slider) {
                        slider.style.left = (x - 25) + "px";
                    }
                    if (divider) {
                        divider.style.left = x + "px";
                    }
                }
                
                // Posição inicial
                moveSlider(w / 2);
                
                // Eventos do slider
                var dragging = false;
                
                function startDrag(e) {
                    dragging = true;
                    activeContainer = container;
                    activeSlider = slider;
                    slider.classList.add('dragging');
                    e.preventDefault();
                    e.stopPropagation();
                }
                
                function endDrag() {
                    dragging = false;
                    if (activeSlider) {
                        activeSlider.classList.remove('dragging');
                    }
                    activeContainer = null;
                    activeSlider = null;
                }
                
                function drag(e) {
                    if (!dragging || activeContainer !== container) return;
                    e.preventDefault();
                    var rect = container.getBoundingClientRect();
                    var clientX = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
                    var x = clientX - rect.left;
                    moveSlider(x);
                }
                
                // Remove listeners antigos
                var newSlider = slider.cloneNode(true);
                slider.parentNode.replaceChild(newSlider, slider);
                slider = newSlider;
                
                slider.addEventListener('mousedown', startDrag);
                slider.addEventListener('touchstart', startDrag, {passive: false});
                
                document.addEventListener('mousemove', drag);
                document.addEventListener('touchmove', drag, {passive: false});
                document.addEventListener('mouseup', endDrag);
                document.addEventListener('touchend', endDrag);
                
                // Click no container
                container.addEventListener('click', function(e) {
                    if (e.target === slider || slider.contains(e.target)) return;
                    if (dragging) return;
                    var rect = container.getBoundingClientRect();
                    var clientX = (e.touches && e.touches[0]) ? e.touches[0].clientX : e.clientX;
                    var x = clientX - rect.left;
                    moveSlider(x);
                });
            }
            
            // Aguarda ambas imagens carregarem
            function checkImages() {
                var imagesLoaded = 0;
                var totalImages = 2;
                var hasError = false;
                
                function trySetup(isError) {
                    if (isError) {
                        hasError = true;
                    }
                    imagesLoaded++;
                    if (imagesLoaded >= totalImages) {
                        // Usa requestAnimationFrame para garantir que o layout está pronto
                        requestAnimationFrame(function() {
                            requestAnimationFrame(function() {
                                setTimeout(setup, 100);
                            });
                        });
                    }
                }
                
                // Verifica se as imagens já estão carregadas
                if (baseImg.complete && baseImg.naturalWidth > 0) {
                    trySetup();
                } else {
                    baseImg.addEventListener('load', function() {
                        trySetup();
                    }, {once: true});
                    baseImg.addEventListener('error', function(e) {
                        trySetup('base');
                    }, {once: true});
                }
                
                if (overlayImg.complete && overlayImg.naturalWidth > 0) {
                    trySetup();
                } else {
                    overlayImg.addEventListener('load', function() {
                        trySetup();
                    }, {once: true});
                    overlayImg.addEventListener('error', function(e) {
                        trySetup('overlay');
                    }, {once: true});
                }
                
                // Timeout de segurança: força inicialização após 5 segundos
                setTimeout(function() {
                    if (imagesLoaded < totalImages) {
                        imagesLoaded = totalImages;
                        setTimeout(setup, 100);
                    }
                }, 5000);
                
                // Força recalcular após um delay para garantir que o layout está pronto
                setTimeout(function() {
                    var testWidth = container.getBoundingClientRect().width;
                    if (testWidth > 0 && testWidth < 10) {
                        setTimeout(setup, 500);
                    }
                }, 1000);
            }
            
            checkImages();
        });
    }
    
    // Inicializa
    function startInit() {
        initComparisons();
        // Aguarda mais tempo para garantir que o layout está pronto
        setTimeout(initComparisons, 500);
        setTimeout(initComparisons, 1000);
        setTimeout(initComparisons, 2000);
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', startInit);
    } else {
        startInit();
    }
    
    window.addEventListener('load', function() {
        setTimeout(initComparisons, 500);
        setTimeout(initComparisons, 1500);
    });
    
    // Força recalcular quando a janela é redimensionada
    window.addEventListener('resize', function() {
        setTimeout(initComparisons, 100);
    });
    
    // Expor função globalmente para debug
    window.initComparisons = initComparisons;
})();

/* Scroll Reveal Suave */
function reveal() {
    var reveals = document.querySelectorAll(".reveal");
    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;
        var elementVisible = 100;
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add("active");
        }
    }
    
    // Fade in para elementos com essa classe
    var fadeIns = document.querySelectorAll(".fade-in");
    for (var i = 0; i < fadeIns.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = fadeIns[i].getBoundingClientRect().top;
        var elementVisible = 100;
        if (elementTop < windowHeight - elementVisible) {
            fadeIns[i].style.opacity = "1";
            fadeIns[i].style.transform = "translateY(0)";
        }
    }
}

// Throttle para melhor performance
let ticking = false;
function optimizedReveal() {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            reveal();
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener("scroll", optimizedReveal, { passive: true });
reveal();

/* Parallax Effect para os Doodles */
document.addEventListener("mousemove", (e) => {
    const doodles = document.querySelectorAll(".parallax");
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    doodles.forEach(doodle => {
        const speed = doodle.getAttribute("data-speed");
        const xOffset = (window.innerWidth - x * 100 * speed) / 100;
        const yOffset = (window.innerHeight - y * 100 * speed) / 100;
        
        doodle.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
});

/* Smooth Scroll para links âncora */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});


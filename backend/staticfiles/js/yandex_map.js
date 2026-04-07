window.addEventListener('map:init', function (e) {
    var detail = e.detail;
    var map = detail.map;

    function initYandex() {
        // Проверяем, загрузились ли обе библиотеки
        if (typeof ymaps !== 'undefined' && typeof L.Yandex !== 'undefined') {
            
            // Удаляем стандартный слой OSM
            map.eachLayer(function (layer) {
                if (layer instanceof L.TileLayer) {
                    map.removeLayer(layer);
                }
            });

            // Добавляем Яндекс (тип 'map' - схема, 'satellite' - спутник)
            var yandexLayer = new L.Yandex('map');
            map.addLayer(yandexLayer);
            
            // Принудительно обновляем размер, чтобы не было серых кусков
            setTimeout(function() { map.invalidateSize(); }, 500);
            
            console.log("Yandex Map Loaded!");
        } else {
            // Если еще не загрузилось, ждем 300мс и пробуем снова
            setTimeout(initYandex, 300);
        }
    }

    initYandex();
}, false);
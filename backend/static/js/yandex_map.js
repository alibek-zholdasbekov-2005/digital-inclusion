window.addEventListener('map:init', function (e) {
    var detail = e.detail;
    var map = detail.map;

    function initYandex() {
        if (typeof ymaps !== 'undefined' && typeof L.Yandex !== 'undefined') {
            
            map.eachLayer(function (layer) {
                if (layer instanceof L.TileLayer) {
                    map.removeLayer(layer);
                }
            });

            var yandexLayer = new L.Yandex('map');
            map.addLayer(yandexLayer);
            
            setTimeout(function() { map.invalidateSize(); }, 500);
            
            console.log("Yandex Map Loaded!");
        } else {
            setTimeout(initYandex, 300);
        }
    }

    initYandex();
}, false);
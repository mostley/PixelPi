var Table = {
    
    ledData: [],
            
    hexToRGB: function (hex) {
        hex = parseInt(((hex.indexOf('#') > -1) ? hex.substring(1) : hex), 16);
        return { R: hex >> 16, G: (hex & 0x00FF00) >> 8, B: (hex & 0x0000FF) };
    },
            
    rgbToHex: function (color) {
        if (color.substr(0, 1) === '#') {
            return color;
        }
        var digits = /(.*?)rgb\((\d+), (\d+), (\d+)\)/.exec(color);

        var red = parseInt(digits[2]);
        var green = parseInt(digits[3]);
        var blue = parseInt(digits[4]);

        var hex = [
            red.toString(16),
            green.toString(16),
            blue.toString(16)
        ];
        $.each(hex, function (nr, val) {
            if (val.length == 1) {
                hex[nr] = '0' + val;
            }
        });
        return '#' + hex.join('');
    },

    getCssColor: function (c) {
        return "rgb(" + c["R"] + ", " + c["G"] + ", " + c["B"] + ")";
    },

    foreachLed: function (func) {
        for (var i = 0; i < 105; i++) {
            Table.ledData[i] = func(i);
        }

        Table.updateTable();
    },
            
    turnAllLedsOff: function () {
        Table.foreachLed(function () { return Table.hexToRGB('#000000'); });
    },
            
    updateTable: function () {
        // TODO buffer?
        $.post('/table/leds', { leds: Table.ledData }, function () {
            //TODO display server/table health
        }, "json");
    },
    
    init: function(onLoaded) {
        $.get('/table/leds', function (data) {
            Table.ledData = data;

            onLoaded();
        });
    }
};
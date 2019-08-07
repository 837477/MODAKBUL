/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <tannern@gmail.com> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  Tanner Netterville
 * ----------------------------------------------------------------------------
 */


function rgbToHsv(r, g, b){
    r = r/255, g = g/255, b = b/255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, v = max;

    var d = max - min;
    s = max == 0 ? 0 : d / max;

    if(max == min){
        h = 0; // achromatic
    }else{
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [Math.round(h * 360), s, v];
}

function hsvToRgb(h, s, v){
    var r, g, b;
    var i;
    var f, p, q, t;
    
    while (h < 0) { h += 360; };
    while (h > 360) { h -= 360; };
    s = Math.max(0, Math.min(1, s));
    v = Math.max(0, Math.min(1, v));
 
    if(s == 0) {
        r = g = b = v;
        return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
    }
 
    h /= 60;
    i = Math.floor(h);
    f = h - i;
    p = v * (1 - s);
    q = v * (1 - s * f);
    t = v * (1 - s * (1 - f));
 
    switch(i) {
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        default: r = v; g = p; b = q;
    }
 
    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}

function hsvToHex(h,s,v){
    var rgb = hsvToRgb(h,s,v);
    return rgbToHex(rgb[0], rgb[1], rgb[2]);
};

function hexToRgb(hex) {
    if (hex.substring(0,1) == '#') { hex = hex.substring(1,hex.length); };
    
    var strPattern = /^([0-9a-f]{3}|[0-9a-f]{6})$/i; 
    if(strPattern.test(hex) == true) {
        if (hex.length == 3) {
            var r = hex.substring(0,0);
            var g = hex.substring(1,1);
            var b = hex.substring(2,2);
            hex = r + r + g + g + b + b;
        };
        var r = parseInt(hex.substring(0,2), 16);
        var g = parseInt(hex.substring(2,4), 16);
        var b = parseInt(hex.substring(4,6), 16);
        return [r, g, b];
    } else {
        return false;
    };
};

function rgbToHex(r,g,b) {
    r = parseInt(r).toString(16);
    g = parseInt(g).toString(16);
    b = parseInt(b).toString(16);
    if (r.length < 2) { r = '0' + r; };
    if (g.length < 2) { g = '0' + g; };
    if (b.length < 2) { b = '0' + b; };
    return r + g + b;
};

jQuery.ColorPicker = function(container, options) {
    var picker = this;
    
    picker.build = function(){
        // Container setup
        var container = picker.el.container
            .empty()
            .css({
                'display': 'block',
                'position': 'relative',
                'width': '272px',
                'height': '272px',
                'margin': 'auto'
            });
        
        // Wheel setup
        var wheel_container = picker.el.wheel_container = jQuery('<div/>')
            .css({
                'position': 'absolute',
                'z-index': '201',
                'top': '8px',
                'left': '8px',
                'width': '272px',
                'height': '272px;'
            }).appendTo(container);
        var wheel = picker.el.wheel = jQuery('<div/>')
            .css({
                'position': 'absolute',
                'z-index': '202',
                'top': '0',
                'left': '0',
                'width': '256px',
                'height': '256px',
                'background': 'url(../static/js/color/jquery.colorpicker.wheel.png)'
            }).appendTo(wheel_container);
        var wheel_mask = picker.el.wheel_mask = jQuery('<div/>')
            .css({
                'position': 'absolute',
                'z-index': '203',
                'top': '0',
                'left': '0',
                'width': '256px',
                'height': '256px',
                'background': 'url(../static/js/color/jquery.colorpicker.wheel_mask.png)',
                'opacity': 0
            }).appendTo(wheel_container);
        var wheel_cursor = picker.el.wheel_cursor = jQuery('<div/>')
            .css({
                'position': 'absolute',
                'z-index': '204',
                'top': '120px',
                'left': '120px',
                'width': '16px',
                'height': '16px',
                'background': 'url(../static/js/color/jquery.colorpicker.wheel_cursor.png)'
            }).appendTo(wheel_container);
        var wheel_hit = picker.el.wheel_hit = jQuery('<div/>')
            .css({
                'position': 'absolute',
                'z-index': '205',
                'top': '-8px',
                'left': '-8px',
                'width': '272px',
                'height': '272px'
            }).appendTo(wheel_container);
        // events
        wheel_cursor.click(function(){return false;});
        wheel_cursor.mousedown(function(){return false;});
        wheel_hit.mousedown(function(){ picker.mouse.wheel = true; });
        wheel_hit.mouseup(function(){ picker.mouse.wheel = false; });
        wheel_hit.mouseout(function(){ picker.mouse.wheel = false; });
        wheel_hit.click(function(e){ picker.wheel_update(e); });

        // 모바일 일떄
        $(document).ready(function() {
            wheel_hit.bind('touchstart', function(e) {
                var target = e.originalEvent.changedTouches;
                picker.mouse.wheel = true;
            });
            wheel_hit.bind('touchmove', function(e) {
                var target = e.originalEvent.changedTouches;
                if (picker.mouse.wheel) {picker.wheel_update_mobile(e);};
            });
            wheel_hit.bind('touchend', function(e) {
                var target = e.originalEvent.changedTouches;
                picker.wheel_update_mobile(e);
                picker.mouse.wheel = false;
            });
        });


        
        jQuery(window).mousemove(function(e){
            if (picker.mouse.wheel) { picker.wheel_update(e); };
        });

        // if jQuery mousewheel is loaded add scrollwheel events
        if (jQuery.fn.mousewheel){
            jQuery(document).keydown(function(e) { if (e.which == 16) { picker.io.shift = true; }});
            jQuery(document).keyup(function(e) { if (e.which == 16) { picker.io.shift = false; }});
            wheel_hit.mousewheel(function(e, rawDelta){
                if (rawDelta < 0) { delta = -1; }
                else if (rawDelta > 0) { delta = 1; }
                if (!picker.io.shift) {
                    var hue = picker.color.hue = picker.color.hue + delta * 0.5;
                    while (hue < 0) {hue += 360;}
                    while (hue > 360) {hue -= 360;}
                    picker.color.hue = hue;
                } else {
                    picker.color.sat = Math.max(0, Math.min(1, picker.color.sat + delta * 0.008));
                };
                picker.update_hex();
                picker.update_hue();
                picker.update();
            }, true);
        };
        
        return picker;
    };
    
    picker.wheel_update = function(e) {
        var x = Math.max(0, Math.min(255, e.pageX - Math.round(picker.el.wheel.offset().left)));
        var y = Math.max(0, Math.min(255, e.pageY - Math.round(picker.el.wheel.offset().top)));
        var d = Math.sqrt(Math.pow(x-picker.math.center.x,2) + Math.pow(y-picker.math.center.y,2));
        if (d <= picker.math.radius) {
            picker.el.wheel_cursor.css({'top': y-8+'px', 'left': x-8+'px'});
            var angle = picker.math.angle = Math.atan2((picker.math.center.y - y), (picker.math.center.x - x));
            var hue = picker.color.hue = Math.round(angle * 180/Math.PI) + 90;
            if (hue < 0) { hue = picker.color.hue += 360; };
            picker.color.sat = d/128;
            
            picker.update_hex();
            
            
            picker.update();
        };
        return picker;
    };
    picker.wheel_update_mobile = function(e) {
        var x = Math.max(0, Math.min(255, e.originalEvent.changedTouches[0].pageX - Math.round(picker.el.wheel.offset().left)));
        var y = Math.max(0, Math.min(255, e.originalEvent.changedTouches[0].pageY - Math.round(picker.el.wheel.offset().top)));
        var d = Math.sqrt(Math.pow(x-picker.math.center.x,2) + Math.pow(y-picker.math.center.y,2));
        if (d <= picker.math.radius) {
            picker.el.wheel_cursor.css({'top': y-8+'px', 'left': x-8+'px'});
            var angle = picker.math.angle = Math.atan2((picker.math.center.y - y), (picker.math.center.x - x));
            var hue = picker.color.hue = Math.round(angle * 180/Math.PI) + 90;
            if (hue < 0) { hue = picker.color.hue += 360; };
            picker.color.sat = d/128;
            
            picker.update_hex();
            
            
            picker.update();
        };
        return picker;
    };
    picker.hex_update = function(hex) {
        if (hex.substring(0,1) == '#') { hex = hex.substring(1,hex.length); };
        
        var rgb = hexToRgb(hex);
        var hsv = rgbToHsv(rgb[0], rgb[1], rgb[2]);
        
        picker.color.hex = hex;
        picker.color.hue = hsv[0];
        picker.color.sat = hsv[1];
        picker.color.val = hsv[2];
        
        picker.update_val();
        picker.update_hue();
        picker.update();
    };
    
    picker.update_hex = function() {
        picker.color.hex = hsvToHex(picker.color.hue, picker.color.sat, picker.color.val);
    };
    
    picker.update_val = function() {
        var top =  256 * (1 - picker.color.val) - 8;
        picker.el.wheel_mask.css('opacity', 0);
    };
    
    picker.update_hue = function() {
        var adeg = picker.color.hue + 90;
        if (adeg < 0) { adeg += 360; };
        var arad = adeg * Math.PI/180;
        var x2 = picker.math.center.x + Math.round(picker.color.sat * picker.math.radius * Math.cos(arad));
        var y2 = picker.math.center.y + Math.round(picker.color.sat * picker.math.radius * Math.sin(arad));
        picker.el.wheel_cursor.css({
            'top': y2 - 8 + 'px',
            'left': x2 - 8 + 'px'
        });
        var fullVal = hsvToHex(picker.color.hue, picker.color.sat, 1);
    };
    picker.update_sat = picker.update_hue;
    
    picker.update = function() {
        picker.update_hex();
        picker.fn.change('#' + picker.color.hex);
    };
    picker.change = picker.update;
    
    picker.hex = function(hex) {
        var strPattern = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i; 
        if (hex && strPattern.test(hex)) {
            picker.hex_update(hex);
            return picker;
        } else {
            return '#' + picker.color.hex;
        };
    };
    
    picker.init = function(){
        var container = arguments[0];
        var options = (arguments[1]) ? arguments[1] : {};
        
        picker.settings = jQuery.extend({
            color: '#aaaaaa',
            change: function(hex){}
        }, options);
        
    
        picker.fn = {};
        picker.fn.change = picker.settings.change;
        picker.el = {};
        picker.el.container = jQuery(container);
        picker.io = {shift: false};
        picker.mouse = {wheel: false};
        picker.math = {};
        picker.math.angle = 0;
        picker.math.center = {x: 128, y: 128};
        picker.math.radius = 128;
        picker.color = {};
        picker.color.hue = 0;
        picker.color.sat = 0;
        picker.color.val = 1;
        picker.color.hex = "ffffff";
        picker.build().hex(picker.settings.color);
        return picker;
    };
    return picker.init(container, options);
};

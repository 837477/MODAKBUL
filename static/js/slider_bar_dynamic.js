var today_ajax;
//===========================================
//스크롤을 통한 동적 변환 함수들
Date.prototype.format = function (f) {
    if (!this.valueOf()) return " ";
    var weekKorName = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
    var weekKorShortName = ["일", "월", "화", "수", "목", "금", "토"];
    var weekEngName = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekEngShortName = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var d = this;
    return f.replace(/(yyyy|yy|MM|dd|KS|KL|ES|EL|HH|hh|mm|ss|a\/p)/gi, function ($1) {
         switch ($1) {
  
            case "yyyy": return d.getFullYear(); // 년 (4자리)
  
            case "yy": return (d.getFullYear() % 1000).zf(2); // 년 (2자리)
  
            case "MM": return (d.getMonth() + 1).zf(2); // 월 (2자리)
  
            case "dd": return d.getDate().zf(2); // 일 (2자리)
  
            case "KS": return weekKorShortName[d.getDay()]; // 요일 (짧은 한글)
  
            case "KL": return weekKorName[d.getDay()]; // 요일 (긴 한글)
  
            case "ES": return weekEngShortName[d.getDay()]; // 요일 (짧은 영어)
  
            case "EL": return weekEngName[d.getDay()]; // 요일 (긴 영어)
  
            case "HH": return d.getHours().zf(2); // 시간 (24시간 기준, 2자리)
  
            case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2); // 시간 (12시간 기준, 2자리)
  
            case "mm": return d.getMinutes().zf(2); // 분 (2자리)
  
            case "ss": return d.getSeconds().zf(2); // 초 (2자리)
  
            case "a/p": return d.getHours() < 12 ? "오전" : "오후"; // 오전/오후 구분
  
            default: return $1;
  
        }
  
    });
  
  };
  String.prototype.string = function (len) { var s = '', i = 0; while (i++ < len) { s += this; } return s; };
  
  String.prototype.zf = function (len) { return "0".string(len - this.length) + this; };
  
  Number.prototype.zf = function (len) { return this.toString().zf(len); };
  
  
  let app = (() => {
  
    function updateSlider(element) {
      if (element) {
        let parent = element.parentElement,
          lastValue = parent.getAttribute('data-slider-value');
  
        if (lastValue === element.value) {
          return; // No value change, no need to update then
        }
        
        //element.value 가 스크롤변화에 따라 진짜 동적으로 값이 계속 변화됨.
        var d = new Date();
        d.setDate((d.getDate()+1)*1 + element.value*1);
  
        var today_ = d.format('yyyy-MM-dd (KS)');
        today_ajax = d.format('yyyy-MM-dd');
        
        parent.setAttribute('data-slider-value', element.value);
        let $thumb = parent.querySelector('.range-slider__thumb'),
          $bar = parent.querySelector('.range-slider__bar'),
          pct = element.value * ((parent.clientHeight - $thumb.clientHeight) / parent.clientHeight);
  
        $thumb.style.bottom = `${pct}%`;
        $bar.style.height = `calc(${pct}% + ${$thumb.clientHeight/2}px)`;
        $thumb.textContent = `${today_}`;
      }
    }
    return {
      updateSlider: updateSlider
    };
  
  })();
  
  (function initAndSetupTheSliders() {
    const inputs = [].slice.call(document.querySelectorAll('.range-slider input'));
    inputs.forEach(input => input.setAttribute('value', '0'));
    inputs.forEach(input => app.updateSlider(input));
    // Cross-browser support where value changes instantly as you drag the handle, therefore two event types.
    inputs.forEach(input => input.addEventListener('input', element => app.updateSlider(input)));
    inputs.forEach(input => input.addEventListener('change', element => app.updateSlider(input)));
  })();
  //스크롤 날짜 변환 동적 함수들
  //==============================================
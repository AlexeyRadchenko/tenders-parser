 // Переменные для восстановления корректного значения в ЛОВ-е
 var last_obj;
 var last_value='';
 var semaf=false;
 // Массив хранения зависимостей
 var lovDepArray= new Array();

function is_IE(){
  if (navigator.appName == "Microsoft Internet Explorer") return true
  else return false;
}
 
// Получить имя класса
function lovClass(p_obj) {
  if (p_obj.className.indexOf('apxLovCorrect')>=0) {
    return 'apxLovCorrect'
  } else {
    return 'apxLovNotCorrect';
  }
}

// Установить класс
function setLovClass(p_obj, p_newClass) {
  var v_className = p_obj.className;
  if (p_newClass=='apxLovCorrect') {
    p_obj.className = v_className.replace(/apxLovNotCorrect/g,'apxLovCorrect');
  } else {
    p_obj.className = v_className.replace(/apxLovCorrect/g,'apxLovNotCorrect');
  }
}
 
// Восстановление последнего корректного значения в лов-е
function setLastValue()
{ 
  if (semaf==true) {
    if (last_obj) {
	  if (lovClass(last_obj)=="apxLovNotCorrect") {
        last_obj.value=last_value;
        setLovClass(last_obj, "apxLovCorrect");
        semaf=false;
	  }
	}
  }
}

/*
// ОБЫЧНАЯ ВЕРСИЯ
function onLovBlur(obj)
{
  if (obj.className=="apxLovNotCorrect") {
    semaf=true;
    window.setTimeout('setLastValue()',5);
  }
//  document.activeElement.style.backgroundColor = '#FF5555';
//  alert(document.activeElement);
//  alert($x('lovAjax').active);
  if ($(document.activeElement ).parents('#lovAjax').size()==1) alert('true'); else alert('false');
}
*/

// ВЕРСИЯ ДЛЯ ПОДДЕРЖКИ AJAX-ных ЛОВ-ов
function onLovBlur(obj)
{
  if (lovClass(obj)=="apxLovNotCorrect") {
    if (!($(document.activeElement).parents('#lovAjax').size()==1)) {
      semaf=true;
      window.setTimeout('setLastValue()',5);
    }  
  }
}


/*
// ОБЫЧНАЯ ВЕРСИЯ
function onEnter(evt, obj)
{
  //alert(evt.keyCode);
  if (evt.keyCode == 13) {
    window.setTimeout('semaf=false;',1);
    showPopupLov(obj.id);  
  }
  else
  if ((evt.keyCode != 9) && (evt.keyCode != 45) && (evt.keyCode != 16)) 
    if (obj.className=="apxLovCorrect") {
      last_obj=obj;
      last_value=obj.value;
      obj.className="apxLovNotCorrect";
    }
}
*/

// ВЕРСИЯ ДЛЯ ПОДДЕРЖКИ AJAX-ных ЛОВ-ов
function onEnter(evt, obj)
{
  //alert(evt.keyCode);
  if (evt.keyCode == 13) {
    if (curLovRow) {
      lovSetValue(curLovRow);
      curLovRow='';
    }
    else {
      window.setTimeout('semaf=false;',1);
      showPopupLov(obj.id);
    }  
  }
  else 
  if (evt.keyCode == 38) {
    lovPrevRow();
  }
  else
  if (evt.keyCode == 40) {
    lovNextRow();
  }
  else
  if ((evt.keyCode != 9) && (evt.keyCode != 45) && (evt.keyCode != 16)) {
    if (lovClass(obj)=="apxLovCorrect") {
      last_obj=obj;
      last_value=obj.value;
      setLovClass(obj, "apxLovNotCorrect");
    }
    if (curLovRow) {
      lovUnsel(curLovRow);
      curLovRow='';
    }
  }  
}

// Кодирует текст для передачи по URL в качестве параметра
function encodeApxURL(v_text) {
  var v_res = v_text;
  v_res = v_res.replace(/,/g,'*$');
  v_res = v_res.replace(/:/g,'*q');
  v_res = v_res.replace(/"/g,'*h');
  v_res = v_res.replace(/%/g,'*j');
  v_res = encodeURI(v_res);
  return v_res;
}

// Функция, предшествующая нажатию на вызов Лов-а
// (чтобы не возвращать в этом случае последнее корректное значение)
function lovMD(obj_id){
  if (last_obj)
    if (last_obj.id == obj_id){
      window.setTimeout('semaf=false;',0);
    }
}

function execOnChangeLov(obj) {    
    var nd = obj.attributes['onChangeVal'];
    if (nd) eval(nd.nodeValue);
}


function changeLovValue(objR, objD) {    
    
	//Если предусмотрено выполнение функций, то они выполняются
	// (они хранятся в атрибуте onChangeVal)
	if (objD) execOnChangeLov(objD);

	// Множество обработанных ЛОВ-ов (защита от зацикливания)
	var usedSet = new Array(objR.id);
	//Стек еще не обработанных зависимых ЛОВ-ов
	var stack = new Array();

	var mainLov = objR.id;
	var depArray;
	var v_change;
  var lov;

	while (mainLov) 
	{
	  depArray = lovDepArray[mainLov];
	  if (depArray) {
	    for (i=0; i<depArray.length; i++) {
		    lov = depArray[i];
		    if (!usedSet[lov]) {
			  //if ($x(lov).value) 
			  if (!isValidLov($x("ll"+lov))) {
    		      v_change = clearLovValue($x("ll"+lov));
				  if (v_change) execOnChangeLov($x("ll"+lov));
                  stack.push(lov);
			  }
			  usedSet[lov]="true";
            }
	    }  
	  }
	  mainLov = stack.pop();  
	}	
}


function onLovFocus()
{
//  setLastValue(); 
}


//-------------------------------------------------------------------------
// Заполнение параметров значениями со страницы
//-------------------------------------------------------------------------
function lovParamValues(params) {
  var param_values="";
  var elem; 

  if (params) {
    params = params.split('^');
    for (var i=1; i<params.length; i++) { 
      elem = $v(params[i]); // $x(params[i]);
//      if (elem) {
        if (i==1) {param_values=param_values + elem;} // elem.value;} 
        else      {param_values=param_values +"^"+ elem;} //elem.value;}
//      }
//      else {if (i>1) param_values=param_values +"^";}
    } 
  }
  return param_values;
}

//---------------------------------------------------------------------------
// Дата со страницы (MDM)
//---------------------------------------------------------------------------
function lovContextDate(obj){
  var v_context_date;
  if ($x('pFlowStepId').value=='3921') {
    var v_idx = $(obj).parents('td[idx]').eq(0).attr('idx');
    if (v_idx) {
      return $x('cardDate_'+v_idx).value;
    } else {
      return $x('P3921_ADD_DATE').value;
    }
  }
  
  try {
    if ($x('cardGlobalDate')) {
      v_context_date = $x('cardGlobalDate').value;
    }
    else {
      if ($x('P'+$x('pFlowStepId').value+'_DATE')) {    
        v_context_date = $x('P'+$x('pFlowStepId').value+'_DATE').value;
      }
      else v_context_date = $x('GLB_GLOBAL_DATE').value;
    }
  }
	catch (e) { v_context_date = ''}
  return v_context_date;
}
 
//---------------------------------------------------------------------------
// Атрибут, для которого вызывается лов (MDM)
//---------------------------------------------------------------------------
function lovContextAttr(obj){
  var attr_id;
  try {
    if (obj.attributes['lovAttrId']) {
      attr_id = obj.attributes['lovAttrId'].nodeValue;
    }
    else
      attr_id = '';
  }
	catch (e) { attr_id = ''}  
  return attr_id;
}

 
//---------------------------------------------------------------------------
// Обработка нажатия на вызов LOV-а
//---------------------------------------------------------------------------
function showPopupLov(obj_id)
{ 
  var obj = $x(obj_id);
  
  var lov_id     = obj.getAttribute('lovId');
  var lov_func   = obj.getAttribute('lovFunc');
  var use_id     = obj.getAttribute('lovUseId');
  var value_id   = obj.getAttribute('lovValueId');
  var label_id   = obj.getAttribute('lovLabelId');
  var params     = obj.getAttribute('lovParams');
  var setting_id = obj.getAttribute('lovSettingId');
  var title      = obj.getAttribute('lovTitle');
  var is_multi   = obj.getAttribute('lovIsMulti');
  var max_count  = obj.getAttribute('lovValCnt');
  if (!max_count) {max_count = ''}
  
  if (lov_id==-1) {alert('Запрос не найден!'); return;}

  var res="";
  if (!title) title='';

  //Заполнение параметров значениями со страницы
  var param_values=lovParamValues(params);
  
  //Заполнение даты и справочника
  var v_context_date = lovContextDate(obj);
  var v_context_attr = lovContextAttr(obj);
  
  
  // Если выполнены нужные условия, то AJAX
  if (lovClass($x(label_id))=="apxLovNotCorrect")
  {
    var first_chars = $x(label_id).value;

    var ajax = new htmldb_Get(null,$x('pFlowId').value,
                              'APPLICATION_PROCESS=APX_LOV_EXEC', $x('pFlowStepId').value);
    ajax.add('GLB_LOV_ID',lov_id);
    ajax.add('GLB_LOV_FUNC',lov_func);
    ajax.add('GLB_LOV_PARAMS',param_values);
    ajax.add('GLB_LOV_FCHAR',first_chars);
    ajax.add('GLB_LOV_USE',use_id);
    ajax.add('GLB_LOV_DATE',v_context_date);
    ajax.addParam('x06',setting_id);
    ajax.addParam('x07',v_context_attr);
    
    res = ajax.get();

    if (res == 'error') {alert('Ошибка в запросе LOV!'); return;};
    if (res != '') {
      var resArr = res.split('::');
    
      $x(value_id).value = resArr[0];
      $x(label_id).value = resArr[1];
      setLovClass($x(label_id), "apxLovCorrect");
      changeLovValue($x(value_id),$x(label_id));
    }
  }
  // Если AJAX нашел более одного знач. или не выполнялся, то вызов страницы                         
  if (res == '')
  {
    if (lovClass($x(label_id))=="apxLovCorrect") first_chars='';
    
    // ТЕСТ. АЯКСНЫЕ ЛОВЫ
    if ((is_multi==0) && ((GLOBAL.APP_USER=='L001_ALEX_')||(GLOBAL.APP_USER=='L001_TANYA_')))
    {
      curLov = obj;
      
      lov.init(lov_id, use_id, param_values, 1/*NUM_RUN*/, setting_id,
               $x(value_id).value, 
               0 /*USE_FAVORITE*/, v_context_date, v_context_attr, title, 
               is_multi, first_chars);
      lov.show();
      return;
    }
    
	// положение и размер окна
	var windowWidth = 565;
	var windowHeight = 450;

	var posX = (screen.width - windowWidth)/2;
	var posY = (screen.height - windowHeight)/2;
	
    var popupURL="f?p="+$x('pFlowId').value+":49:"+$x('pInstance').value+
	       "::::P49_QUERY_ID,P49_QUERY_FUNC,P49_USE_ID,P49_RETURN,P49_DISPLAY,"+
         "P49_PAGE_ID,"+  // ***
         "P49_PARAMS,P49_NUM_RUN,P49_EXTRA_SET,P49_CUR_VALUE,P49_USE_FAVORITE,"+
         "P49_CONTEXT_DATE,P49_CONTEXT_ATTR,P49_DISPLAY_MULTIVAL_COUNT,P49_TITLE"+
         ",P49_MULTI_REF_ID,P49_SEARCH:"
         +lov_id+","+lov_func+","+use_id+","+value_id+","+label_id+","
         +$x('pFlowStepId').value+","  // ***
         +encodeApxURL(param_values)+",1,"+setting_id+","+encodeApxURL($x(value_id).value)
         +",0,"+v_context_date+","+v_context_attr+","+max_count+","+encodeApxURL(title)+","
         +is_multi+","+encodeApxURL(first_chars);
    win = window.open(popupURL,"lov","toolbar=0,location=0,directories=0,"+
      "status=1,menubar=0,Scrollbars=0,resizable=1,left=" + posX + ",top=" + posY + ",height=" + windowHeight + "px,width=" + windowWidth+"px");
    win.focus();
  }
}

//---------------------------------------------------------------------------
// Проверка на Valid-ность 
//---------------------------------------------------------------------------
function isValidLov(obj)
{ 
  var lov_id   = obj.getAttribute('lovId');
  var lov_func = obj.getAttribute('lovFunc');
  var use_id   = obj.getAttribute('lovUseId');
  var value_id = obj.getAttribute('lovValueId');
  var params   = obj.getAttribute('lovParams');
  var is_multi = obj.getAttribute('lovIsMulti');
  
  var param_values=lovParamValues(params);

  var v_multi_prefix="";
  if (is_multi == "1") {v_multi_prefix="$multi";}
  
  var ajax = new htmldb_Get(null,$x('pFlowId').value,
                          'APPLICATION_PROCESS=APX_LOV_VALID', $x('pFlowStepId').value);
  ajax.add('GLB_LOV_ID',lov_id);
  ajax.add('GLB_LOV_FUNC',lov_func);
  ajax.add('GLB_LOV_PARAMS',param_values);
  ajax.add('GLB_LOV_FCHAR',v_multi_prefix + $x(value_id).value);
  ajax.add('GLB_LOV_USE',use_id);
  ajax.add('GLB_LOV_DATE',lovContextDate(obj));
  ajax.addParam('x07',lovContextAttr(obj));
  var res = ajax.get();
  if (res=='valid') {return true} else {return false};
  return;
}

// Очистка значения в лов-е (применяется в зависимых лов-ах)
function clearLovValue(obj)
{
  var value_id = obj.attributes['lovValueId'].nodeValue;
  var is_multi = obj.attributes['lovIsMulti'].nodeValue;
  var v_change = false;
  
  if (is_multi != "1") {
    v_change = (obj.value);
    //Очистка отображаемого значения
    obj.value = "";
    //Очистка возвращаемого значения
    $x(value_id).value = "";  
  }
  // Очистка ЛОВ-а С МУЛЬТИВЫБОРОМ
  else { 
    v_change = (obj.innerHTML);
    obj.innerHTML = "";
    var ajax = new htmldb_Get(null,$x('pFlowId').value,
                        'APPLICATION_PROCESS=APX_LOV_CLEAR_MULTI', $x('pFlowStepId').value);
    ajax.add('GLB_LOV_FCHAR',$x(value_id).value);
    var res = ajax.get();
  }
  return v_change;
}

//---------------------------------------------------------------------------  
// Попытка вставить значение из буфера обмена 
//---------------------------------------------------------------------------
function pasteInLov(obj,evt)
{ 
  var pasteText;
  if (window.clipboardData) {
    pasteText = window.clipboardData.getData("Text");
  }
  var pasteArray = pasteText.split(":");
  if (pasteArray[0]=="$OBRN") 
  {
    var val = pasteArray[2];

	  if (evt) {evt.returnValue=false;}
    
    var lov_id   = obj.attributes['lovId'].nodeValue;
    var lov_func = obj.attributes['lovFunc'].nodeValue;
    var use_id   = obj.attributes['lovUseId'].nodeValue;
    var value_id = obj.attributes['lovValueId'].nodeValue;
    var label_id = obj.attributes['lovLabelId'].nodeValue;
    var params   = obj.attributes['lovParams'].nodeValue;
  
    var param_values=lovParamValues(params);

    var ajax = new htmldb_Get(null,$x('pFlowId').value,
						'APPLICATION_PROCESS=APX_LOV_PASTE', $x('pFlowStepId').value);
    ajax.add('GLB_LOV_ID',lov_id);
    ajax.add('GLB_LOV_FUNC',lov_func);
    ajax.add('GLB_LOV_PARAMS',param_values);
    ajax.add('GLB_LOV_FCHAR',val);
    ajax.add('GLB_LOV_USE',use_id);
    ajax.add('GLB_LOV_DATE',lovContextDate(obj));
    ajax.addParam('x07',lovContextAttr(obj));
    res = ajax.get();
    
    switch(res) {
	  case "$ErrorNotFound" :
        alert("Значение не соответствует списку");
        break;
	  case "$ErrorManyRecord" :
        alert("Найдено несколько значений с данным ID");
        break;
	  case "$ErrorUnknown" :
        alert("Неизвестная ошибка выполнения запроса!");
        break;
    default :
        $x(value_id).value = val;
        $x(label_id).value = res;
		    setLovClass($x(label_id), "apxLovCorrect");
	      changeLovValue($x(value_id), $x(label_id));
        break; 
	  }
  }
  else {
     if (lovClass(obj)=="apxLovCorrect") {
      last_obj=obj;
      last_value=obj.value;
      setLovClass(obj, "apxLovNotCorrect"); 
      //alert("В буфере обмена не то");
	  } 
  } 
}


// Вставить значение в LOV (копия подпрограммы - временно)
function pasteValInLov(obj, val)
{
    var lov_id   = obj.attributes['lovId'].nodeValue;
    var lov_func = obj.attributes['lovFunc'].nodeValue;
    var use_id   = obj.attributes['lovUseId'].nodeValue;
    var value_id = obj.attributes['lovValueId'].nodeValue;
    var label_id = obj.attributes['lovLabelId'].nodeValue;
    var params   = obj.attributes['lovParams'].nodeValue;
  
    var param_values=lovParamValues(params);

    var ajax = new htmldb_Get(null,$x('pFlowId').value,
						'APPLICATION_PROCESS=APX_LOV_PASTE', $x('pFlowStepId').value);
    ajax.add('GLB_LOV_ID',lov_id);
    ajax.add('GLB_LOV_FUNC',lov_func);
    ajax.add('GLB_LOV_PARAMS',param_values);
    ajax.add('GLB_LOV_FCHAR',val);
    ajax.add('GLB_LOV_USE',use_id);
    ajax.add('GLB_LOV_DATE',lovContextDate(obj));
    ajax.addParam('x07',lovContextAttr(obj));
    res = ajax.get();
    
    switch(res) {
	  case "$ErrorNotFound" :
        alert("Значение не соответствует списку");
        break;
	  case "$ErrorManyRecord" :
        alert("Найдено несколько значений с данным ID");
        break;
	  case "$ErrorUnknown" :
        alert("Неизвестная ошибка выполнения запроса!");
        break;
    default :
        $x(value_id).value = val;
        $x(label_id).value = res;
		    setLovClass($x(label_id), "apxLovCorrect");
	      changeLovValue($x(value_id), $x(label_id));
        break; 
	  }
}

//---------------------------------------------------------------------------
// ФАВОРИТЫ применительно к ЛОВ-ам
//---------------------------------------------------------------------------
function showLovFavor(obj_id)
{ 
  var obj = $x(obj_id);

  var lov_id     = obj.getAttribute('lovId');
  var lov_func   = obj.getAttribute('lovFunc');
  var use_id     = obj.getAttribute('lovUseId');
  var value_id   = obj.getAttribute('lovValueId');
  var label_id   = obj.getAttribute('lovLabelId');
  var params     = obj.getAttribute('lovParams');
  var setting_id = obj.getAttribute('lovSettingId');
  var title      = obj.getAttribute('lovTitle');
  var is_multi   = obj.getAttribute('lovIsMulti');
  var max_count  = obj.getAttribute('lovValCnt');
  if (!max_count) {max_count = ''}
  
  if (lovClass($x(label_id))=="apxLovNotCorrect")
    var first_chars = $x(label_id).value
  else 
    var first_chars ="";
  
  
  var param_values=lovParamValues(params);
  var popupURL="f?p="+$x('pFlowId').value+":49:"+$x('pInstance').value
         +"::::P49_QUERY_ID,P49_QUERY_FUNC,"+
         "P49_USE_ID,P49_RETURN,P49_DISPLAY,"+
         "P49_PAGE_ID,"+  // ***
         "P49_PARAMS,P49_NUM_RUN,"+
         "P49_EXTRA_SET,P49_CUR_VALUE,P49_USE_FAVORITE,P49_CONTEXT_DATE,P49_DISPLAY_MULTIVAL_COUNT,P49_TITLE,"+
         "P49_MULTI_REF_ID,P49_SEARCH:"
         +lov_id+","+lov_func+","+use_id+","+value_id+","+label_id+","
         +$x('pFlowStepId').value+","  // ***
         +encodeApxURL(param_values)+",1,"+setting_id+","+encodeApxURL($x(value_id).value)
         +",1,"+lovContextDate(obj)+","+max_count+","+encodeApxURL(title)+","
         +is_multi+","+encodeApxURL(first_chars);
  win = window.open(popupURL,"lov","toolbar=0,location=0,directories=0,"+
      "status=1,menubar=0,scrollbars=0,resizable=1,width=565px, height=450px");
}
  
  
// Список "Зависит от"
function lovParamNames(obj_id) {
  var obj = $x(obj_id);
  if (!obj) {return;}
  
  var params = obj.attributes['lovParams'].nodeValue;
  var param_names = "";
  var elem; 
  var v_exist="";

  if (params) {
    params = params.split('^');
    for (var i=1; i<params.length; i++) { 
      elem = $x('ll'+params[i]);
      if (elem) {
//        if (elem.attributes['lovTitle'].nodeValue) {
		      if (!v_exist) {param_names=param_names + elem.attributes['lovTitle'].nodeValue;} 
          else          {param_names=param_names +",  "+ elem.attributes['lovTitle'].nodeValue;}
          v_exist='1';
//		    }  
      }
      else {if (i>1) {}}
    } 
  }
  return param_names;
}
 

 
 
 
// ******************************************************************* 
// AJAX-ные ЛОВЫ
// ******************************************************************* 
function TLov(array){

  var _this=this;
  
  this.lov_id       ='';  
  this.use_id       ='';
  this.param_values ='';
  this.num_run      ='';
  this.setting_id   ='';
  this.value        ='';
  this.use_favorite =''; 
  this.context_date ='';
  this.context_attr ='';
  this.title        =''; 
  this.is_multi     ='';
  this.first_chars  ='';
  
  // свойства, изменяющиеся при работе лова
  this.show_parents ='';
  this.show_childs  ='';
  this.pagination   =1;
  this.sel_only     ='';
  this.favex_id     ='';
  this.order        ='';
  
  if (array){
    for(var i in array){
      this[i]=array[i];
    }
  }
  
  // ************* МЕТОДЫ *****************
  // Следующий Pagination
  this.sort = function(p_sort) {
    this.order = p_sort;
    this.show();
  }

  // Предыдущий Pagination
  this.prevPagin = function() {
    this.pagination = this.pagination-1;
    this.show();
  }

  // Следующий Pagination
  this.nextPagin = function() {
    this.pagination = this.pagination+1;
    this.show();
  }
  
  // Инициализация
  this.init = function(lov_id, use_id, param_values, num_run, setting_id, p_value, use_favorite, 
                       p_context_date, p_context_attr, title, 
                       is_multi, first_chars) 
  {
    this.lov_id       =lov_id;  
    this.use_id       =use_id;
    this.param_values =param_values;
    this.num_run      =num_run;
    this.setting_id   =setting_id;
    this.value        =p_value;
    this.use_favorite =use_favorite; 
    this.context_date =p_context_date;
    this.context_attr =p_context_attr;
    this.title        =title; 
    this.is_multi     =is_multi;
    this.first_chars  =first_chars;                       
  }
  
  // Добавляет событие
  this.addEvent = function(el, evname, func) {
    if (el.attachEvent) { // IE
      el.attachEvent("on" + evname, func);
    } else if (el.addEventListener) { // Gecko / W3C
      el.addEventListener(evname, func, true);
    } else {
    el["on" + evname] = func;
    }
  }
  
  // Удаляет событие
  this.removeEvent = function(el, evname, func) {
    if (el.detachEvent) { // IE
      el.detachEvent("on" + evname, func);
    } else if (el.removeEventListener) { // Gecko / W3C
      el.removeEventListener(evname, func, true);
    } else {
      el["on" + evname] = null;
    }
  }

  // Обработка клика
  this.checkClick = function(ev) {
    var el;
    if (is_IE()) {
      el = window.event.srcElement;
    } else {
      el = ev.target; //el = ev.originalTarget;
    } 

    //console.debug(ev.target);
    //if (el != curLov) {alert("не равно");}
    
    var v_sz;
    try {
      v_sz = $(el).parents('#lovAjax').size();
    }
    catch (e) {v_sz = 0;};
    
    if ((v_sz != 1) && (el != curLov)) {
      deactivAjaxLov();
      _this.removeEvent(document, "mousedown", _this.checkClick);     // ПОТОМ ПЕРЕНЕСТИ  В МЕТОД "СКРЫТЬ"      Перенести !!!!    Перенести !!!!    Перенести !!!!
    }
  }
  
  // Следующий Pagination
  this.show = function() {
    $.ajax({
        type  : "POST"
      , url   : "wwv_flow.show"
      //, dataType : 'json'  
      , async: true 
      , beforeSend:function(){
        }
      , data  : {
            f01: [this.lov_id
                , this.use_id
                , this.param_values
                , this.num_run
                , this.setting_id
                , this.value
                , this.use_favorite
                , this.context_date
                , this.context_attr
                , this.title
                , this.is_multi
                , this.first_chars
                , this.pagination
                , this.order
                ]
          , p_flow_id       : $x('pFlowId').value
          , p_flow_step_id  : $x('pFlowStepId').value
          , p_instance      : $x('pInstance').value
          , p_request       : 'APPLICATION_PROCESS=APX_LOV_AJAX'
        }
      , success:function(data){
          if (!$x("lovAjax")) {
            $('body').append('<div id="lovAjax" style="position:absolute; display:none; '+
                             'width:350px; background-color:#EEEEEE"></div>'); 
            $('#lovAjax').draggable({containment:$(document.body),handle:'#lovAjax'});
          }

          $x("lovAjax").innerHTML = data;
          if (_this.num_run==1) {
            //$x('lovAjax').style.top = $(curLov).position().top+19;
            //$x('lovAjax').style.left = $(curLov).position().left-2;
            //$x('lovAjax').style.width = curLov.clientWidth;

            $x('lovAjax').style.display = '';
            //*******   Ширина
            if (curLov.clientWidth > 350)
            {
              $x('lovAjax').style.width = curLov.clientWidth;
            }
            else {
              $x('lovAjax').style.width = 350;
            }
            //*******   Горизонтальные координаты
            if (($(curLov).position().left-2 + $x('lovAjax').clientWidth)>document.body.clientWidth)
            {
              $x('lovAjax').style.left = document.body.clientWidth - $x('lovAjax').clientWidth;
            }
            else {
              $x('lovAjax').style.left = $(curLov).position().left-2;
            }
            //*******   Вертикальные координаты
            if (($(curLov).position().top+19 + $x('lovAjax').clientHeight)>document.body.clientHeight)
            {
              $x('lovAjax').style.top = $(curLov).position().top - 3 - $x('lovAjax').clientHeight;
            }
            else {
              $x('lovAjax').style.top = $(curLov).position().top+19;
            }
            //*********************************************
          }

          
            // Обратная связь
          _this.pagination = new Number($x("lovPagin").value);
          _this.order      = $x("lovOrder").value;
          
          // События
          if (_this.num_run==1) {
            _this.addEvent(document, "mousedown", _this.checkClick);
          }

          if ($x("lov").rows.length>1) {
            curLovRow = $x("lov").rows[1];
            lovSel(curLovRow);
          } 
        }
      , complete : function(){
          _this.num_run = _this.num_run +1;
        }
    });   
  }
  
} 
  

  var lov = new TLov();  
  var curLov;
  var curLovRow;
  

function lovSel(obj,ev)
{ 
  obj.style.backgroundColor="#D5F3FF";
}

function lovUnsel(obj,ev)
{
  obj.style.backgroundColor="";
}

// Установка значения, выбранного в лов-е (AJAX-ные ЛОВ-ы)
function lovSetValue(selRow)
{ 
  var objReturn  = $x(curLov.attributes['lovValueId'].nodeValue);
  var objDisplay = $x(curLov.attributes['lovLabelId'].nodeValue);
  var dСol = $x('lovDCol').value;

  if (objReturn) {
    objReturn.value = selRow.cells[0].innerHTML;
  }  
  if (objDisplay) {
    if (is_IE())
      objDisplay.value = selRow.cells[dСol].innerText;
	  else 
	    objDisplay.value = $(selRow.cells[dСol]).text();
    setLovClass(objDisplay, "apxLovCorrect");
  }

  closeAjaxLov();
  changeLovValue(objReturn, objDisplay); 
}

// Закрытие AJAX-ного лова
function closeAjaxLov() {
  $x('lovAjax').style.display = 'none';
  $x("lovAjax").innerHTML = '';
}

// Прокрутка до текущего значения  (для AJAX-ных ЛОВ-ов)
function showCurrentRow(){

if ($x('rCur'))
    document.getElementById('lovDiv').scrollTop=$x('rCur').offsetTop
             -(document.getElementById('lovDiv').clientHeight/2)+10;
}

// Следующая строка (AJAX-ные ЛОВ-ы)
function lovNextRow() {
  if (!curLovRow) return;
/*  
  var tmpRow = curLovRow;
  var tmpClassName;
  do {
    tmpRow = tmpRow.nextSibling;
    if (tmpRow)
      if (tmpRow.attributes)   
        tmpClassName = tmpRow.className;
      else tmpClassName = 'unselRow';  
    else tmpClassName = 'unselRow';  
  } 
  while ((tmpRow)&&(tmpClassName!='selRow'));
  
  if (tmpClassName=='selRow') {
    lovUnsel(curLovRow);
    curLovRow = tmpRow;
    lovSel(curLovRow);
  }
*/

  if (curLovRow.nextSibling) {
    lovUnsel(curLovRow);
    curLovRow = curLovRow.nextSibling;
    lovSel(curLovRow);
  }
  if (document.getElementById('lovDiv').scrollTop<curLovRow.offsetTop-document.getElementById('lovDiv').clientHeight+40) {
    document.getElementById('lovDiv').scrollTop=curLovRow.offsetTop-document.getElementById('lovDiv').clientHeight+40;
  }
}

// Предыдущая строка (AJAX-ные ЛОВ-ы)
function lovPrevRow() {
  if (!curLovRow) return;
/*
  var tmpRow = curLovRow;
  var tmpClassName;
  do {
    tmpRow = tmpRow.previousSibling;
    if (tmpRow)
      if (tmpRow.attributes)   
        tmpClassName = tmpRow.className;
      else tmpClassName = 'unselRow';  
    else tmpClassName = 'unselRow';  
  } 
  while ((tmpRow)&&(tmpClassName!='selRow'));

  if (tmpClassName=='selRow') {
    lovUnsel(curLovRow);
    curLovRow = tmpRow;
    lovSel(curLovRow);
  }
*/  
  if (curLovRow.previousSibling) {
    lovUnsel(curLovRow);
    curLovRow = curLovRow.previousSibling;
    lovSel(curLovRow);
  }
  
  if (document.getElementById('lovDiv').scrollTop>curLovRow.offsetTop-40) {
    document.getElementById('lovDiv').scrollTop=curLovRow.offsetTop-40;
  }
}


function deactivAjaxLov(){
//  if (!($(document.activeElement).parents('#lovAjax').size()==1)) {
    semaf=true;
    setLastValue();
    closeAjaxLov();
    curLovRow='';
//  }  
}


//***************************************************************
//**   Копии функций для AJAX-ных ловов
//***************************************************************
// Предыдущий Pagination
function lovPrevPagin(){
  lov.prevPagin();
}

// Следующий Pagination
function lovNextPagin(){
  lov.nextPagin();
}

// Сортировка
function lovSort(sortParam){
  lov.sort(sortParam);
}

// Количество строк
function lovRowCount(){
  var ajax = new htmldb_Get(null,$x('pFlowId').value,
                            'APPLICATION_PROCESS=APX_LOV_ROW_COUNT', $x('pFlowStepId').value);
  var v_res = ajax.get(); 
  $x('lovRowCount').innerHTML = v_res;
}

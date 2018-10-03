/*region resize (mostly div-based)*/
$.fn.makeResizable=function(params){
  /*dont use this metod for multi object*/
  if (this.size()!=1){
    return this;
  }
  /*its default initialization for basic parameters*/
  var obj=$.extend({
          minWidth:   50
        , minHeight:  50
        , maxWidth:   2000
        , maxHeight:  2000
        , start:      function(){}
        , resize:     function(){}
        , stop:       function(){}
        , genTop:     true
        , useWrap:    true
        , registerID: ''
      }
    , params);
  /*saving pointer to *this* object*/
  var _this=this;
  if (obj.registerID!=''){
    if (Report.customize.rid[obj.registerID]){
      Report.customize.rid[obj.registerID].resize.obj=obj;
    }
  }
  /*saving some dimentions*/
  var objectHeight=_this.get(0).clientHeight;//_this.height();
  var objectWidth=_this.get(0).clientWidth;//_this.width();
  /*if need to wrap around*/
  if (obj.useWrap){
    _this.wrap('<table cellpadding="0" cellspacing="0" class="wrapRegion"><tr><td class="handle-hidable"></td><td class="handle-right"></td></tr><tr><td class="handle-bottom"></td><td class="handle-right-bottom"><div><img src="/'+GLOBAL.GLB_ICO_DIR/*'app8/ico'*/+'/resize/resizable-se.gif"/></div></td></tr></table>');
  }
  /*find first table from *this* object. usualy it is table*/
  var wrapper=_this.parents('table').eq(0);
  /*if need to generate top of wrapper*/
  if (obj.useWrap){
    if (obj.genTop){
      wrapper.prepend('<tr><td class="handle-top"></td><td class="handle-right-top"><img src="/'+GLOBAL.GLB_ICO_DIR/*'app8/ico'*/+'/resize/resizable-ne.gif"/></td></tr>');
    }
    wrapper.height(objectHeight);
    wrapper.width(objectWidth);
  }
  /*defining some handles*/
  var handleRight = $('.handle-right',wrapper);
  var handleBottom = $('.handle-bottom',wrapper);
  var handleRightBottom = $('.handle-right-bottom',wrapper);
  /*variable for selection*/
  var resizableSelection;
  /*variables for inital mouse position*/
  var startX;
  var startY;
  /*indicates that was mouce move or not*/
  var was_move_w=false;
  var was_move_h=false;
  /*function for mouse move*/
  var make_move=function(){
    /*changing resizable dimentions*/
    if (arguments[0].data.type.indexOf('right')!=-1){
      var w_=wrapper.get(0).clientWidth+arguments[0].clientX-startX;
      if ((w_>=obj.minWidth)&&(w_<=obj.maxWidth)){
        resizableSelection.width(w_ + 5) //modified
        was_move_w=true;
      }
    }
    if (arguments[0].data.type.indexOf('bottom')!=-1){
      var h_=wrapper.get(0).clientHeight+arguments[0].clientY-startY;
      if ((h_>=obj.minHeight)&&(h_<=obj.maxHeight)){
        resizableSelection.height(h_ + 5); //modified
        was_move_h=true;
      }
    }
    /*executing object functon*/
    obj.resize.apply(obj,arguments);
    /*prevent default*/
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  /*function for mouse up*/
  var make_up=function(){
    var l_resize={type:"",base_width:0,base_height:0,target_width:0,targer_height:0};
    if (was_move_w){
      /*changing size of *this* and wrapper*/
      l_resize.type+='w';
      l_resize.target_width=resizableSelection.get(0).clientWidth-2;
      l_resize.base_width=_this.width();
      wrapper.css('width',resizableSelection.get(0).clientWidth-2)
      _this.css('width',resizableSelection.get(0).clientWidth-2)
    }
    if (was_move_h){
      l_resize.type+='h';
      l_resize.target_height=resizableSelection.get(0).clientHeight-2;
      l_resize.base_height=_this.height();
      /*changing size of *this* and wrapper*/
      wrapper.css('height',resizableSelection.get(0).clientHeight-2);
      _this.css('height',resizableSelection.get(0).clientHeight-2)
    }
    /*removing seletion*/
    resizableSelection.remove();
    resizableSelection='';
    /*unbind document events*/
    $(document).unbind('.resizeRegion');
    /*executing object functon*/
    obj.stop.apply(obj,[arguments[0],l_resize]);
    was_move_w=false;
    was_move_h=false;
    /*prevent default*/
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  /*function for mouse down*/
  var make_down=function(){
    /*inintializing mouse position*/
    startX=arguments[0].clientX;
    startY=arguments[0].clientY;
    /*creating selection*/
    resizableSelection=$('<div class="resize"/>');
    var pos=wrapper.position()
    resizableSelection
      .css('top',Number(pos.top)/*+(($.browser.msie)?document.body.scrollTop:2)*/+2-4*$.browser.msie)
      .css('left',Number(pos.left)/*+(($.browser.msie)?document.body.scrollLeft:0)-4*/-4+2*$.browser.msie)
      .width(wrapper.get(0).clientWidth)
      .height(wrapper.get(0).clientHeight-4);
    $('body').append(resizableSelection);
    /*binding events to document*/
    $(document)
      .bind('mousemove.resizeRegion',arguments[0].data,make_move)
      .bind('mouseup.resizeRegion',make_up)
      .bind('keydown.resizeRegion',function(e){
        if (e.keyCode==27){
          $(document).unbind('.resizeRegion');
          /*removing seletion*/
          resizableSelection.remove();
          resizableSelection='';
        }
      });
    /*executing object functon*/
    obj.start.apply(obj,arguments);
    /*prevent default*/
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  /*binding events*/
  handleRight.unbind('.resizeRegion').bind('mousedown.resizeRegion',{"type":"right"},make_down);
  handleBottom.unbind('.resizeRegion').bind('mousedown.resizeRegion',{"type":"bottom"},make_down);
  handleRightBottom.unbind('.resizeRegion').bind('mousedown.resizeRegion',{"type":"bottom-right"},make_down);
  return this;
}

/*table column resie*/
$.fn.makeResCols=function(params){
  /*its default initialization for basic parameters*/
  var obj=$.extend({
          minWidth:   10
        , minHeight:  10
        , maxWidth:   2000
        , maxHeight:  2000
        , start:      function(){}
        , resize:     function(){}
        , stop:       function(){}
        , autoSize:   function(){}
      }
    , params);
  /*saving pointer to *this* object*/
  var _this=this;
  //_this.parents('table').eq(0).css('width','auto');
  /*i hate empty th =|*/
  //_this.filter(':empty').append('&nbsp;');
  var cachedDivs=[];
  //find all td in current region
  var divs=$('td.tdScrollData',_this.parents('table').eq(0))//.wrapInner('<div style=""/>');
  /*_this.wrapInner('<table cellpadding="0" cellspacing="0" class="resizable-header"><tr style="position:static;"><td><div class="resizable-header"></div></td><td style="width:3px;"><div class="handle" style="cursor:col-resize;">&nbsp;</div></td></tr></table>').css('padding-right',0);*/
  _this.css('padding-right',0);
  //array of handles
  var handle=[];
  //start mouse position
  var startX;
  var startY;
  var was_move=false;
  var initial_width=0;
  var initial_width_shift=0;
  /*variable for selection*/
  var resizableSelection;
  /*function that calculates sum of widths of THs*/
  var calcWidth=function(p_to){
    var retval=0;
    for(var i=0;i<p_to;i++){
      retval+=_this.get(i).clientWidth;
    }
    return retval;
  }
  /*function for mouse move*/
  var make_move=function(){
    var w_=initial_width+arguments[0].clientX-startX;
    if ((w_>=obj.minWidth)&&(w_<=obj.maxWidth)){
      /*set selection size*/
      resizableSelection.width(w_)
      was_move=true;
    }
    /*executing object function*/
    obj.resize.apply(obj,arguments);
    /*prevent default*/
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  /*function for mouse up*/
  var make_up=function(){
    if (was_move){
      var index=arguments[0].data.index;
      //$('div',_this.eq(index)).eq(0).css('width',resizableSelection.get(0).clientWidth-2)
      /*set header size (table and inner div)*/
      _this.eq(index).children().css('width',resizableSelection.get(0).clientWidth+initial_width_shift-6)
      $('div',_this.eq(index)).eq(0).css('width',resizableSelection.get(0).clientWidth+initial_width_shift-6)
      if (!cachedDivs[index]){
        cachedDivs[index]=divs.filter(function(i){return (Number(i%_this.size())==index)})
      }
      /*resize TDs divs*/
      cachedDivs[index].children().css('width',resizableSelection.get(0).clientWidth+initial_width_shift-3)
    }
    /*removing selection*/
    resizableSelection.remove();
    resizableSelection='';
    /*unbind events*/
    $(document).unbind('.resizeColumn');
    /*executing object function*/
    was_move&&obj.stop.apply(obj,arguments);
    /*prevent default*/
    was_move=false;
    initial_width=0;
    initial_width_shift=0;
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  /*function for mouse down*/
  var make_down=function(){
    /*inintializing mouse position*/
    startX=arguments[0].clientX;
    startY=arguments[0].clientY;
    /*creating selection*/
    resizableSelection=$('<div class="resize"/>');
    var pos=_this.eq(arguments[0].data.index).parents('table').eq(0).position()
    var v_left=Number(pos.left)+Number(calcWidth(arguments[0].data.index))/*+(($.browser.msie)?document.body.scrollLeft:0)*/-2;
    initial_width = _this.get(arguments[0].data.index).clientWidth+1-3*$.browser.mozilla;
    var container=_this.eq(0).parents('div.container');
    var container_position=container.position();
    /*if was some scroll... horizontal*/
    if (v_left<container_position.left){
      var t_left=v_left;
      v_left=container_position.left-2;
      initial_width_shift=v_left-t_left;
      initial_width=Number(initial_width)-v_left+t_left;
    }
    resizableSelection
      .css('top',Number(container_position.top)/*+(($.browser.msie)?document.body.scrollTop:2)*/-2)
      .css('left',v_left)
      .width(initial_width)
      .height(_this.eq(arguments[0].data.index).parents('div').get(0).clientHeight+1);
    
    $('body').append(resizableSelection);
    /*binding document events*/
    $(document)
      .bind('mousemove.resizeColumn',arguments[0].data,make_move)
      .bind('mouseup.resizeColumn',arguments[0].data,make_up)
      .bind('keydown.resizeColumn',function(e){
        if (e.keyCode==27){
          $(document).unbind('.resizeColumn');
          /*removing seletion*/
          resizableSelection.remove();
          resizableSelection='';
        }
      });
    /*executing object function*/
    obj.start.apply(obj,arguments);
    /*prevent default*/
    if (arguments[0].preventDefault) {
      arguments[0].preventDefault();
    } else {
      arguments[0].returnValue = false;
    }
  }
  var make_dbl = function(){
    var index=arguments[0].data.index;
    var l_div=_this.eq(index).children().css('width','100%')
    $('div',_this.eq(index)).eq(0).css('width','auto');
    if (!cachedDivs[index]){
      cachedDivs[index]=divs.filter(function(i){return (Number(i%_this.size())==index)})
    }
    /*resize TDs divs*/
    cachedDivs[index].children().css('width','auto');
//    $('div',_this.eq(index)).eq(0).css('width',t);
    obj.autoSize.apply(obj,arguments);
//    $('div',_this.eq(index)).eq(0).css('width','auto');
  }
  /*initing some handle events*/
  for(var k=0;k<_this.size();k++){
    handle[k]=$('.handle',$(_this.eq(k)));
    handle[k].bind('mousedown',{"index":k,"objects":_this},make_down);
    handle[k].bind('dblclick',{"index":k,"objects":_this},make_dbl);
  }
  return this;
}

/**/
var timeOutString=''

Array.prototype.indexOf=function(elem){
  for (var i=0;i<this.length;i++){
    if (this[i]==elem) return i
  }
  return -1
}

var freezedObjects=new Array()
/*
  ��� ������� ���� ��������
*/
function timeOutClear(){
  for (i in timeOutString.split(':')){
    clearTimeout(i)
  }
}

/*
  �����������
*/
function ToolTip(array){
  //������ �� ����
  var GLOBAL_THIS         = this;
  //��� ����������. ��� ���������� �������
  this.VAR_NAME           = 'toolTip'
  
  // �������� ������ �������� �������
  this.hideInterval       = null;
  
  // ��� ��������� � ��� �����
  this.divToolTip         = null;
  this.divToolTipScroll   = null;
  this.divToolTipInner    = null;
  
  // ������ �������\���������� �������
  this.enableToolTips     = true;
  
  // ������� ����, ��� ������ ������ ������������
  this.isShownTip         = false;
  // ������� ����, ��� ����� � �������
  this.isMouseInDiv       = false;
  // ������� ������, ��� �������� ����������� mouseover
  this.activeObject       = null;
  // ���������� ������, ��� �������� ������������ ���������
  this.prevActiveObject   = null;
  // ������������� ������ ������ ����������� ���������
  this.cnt                = 0;
  // ������� ����� ������ ������� ��� ���������
  this.xpos               = 0;
  this.ypos               = 0;
  // ��������� �������� ������ � ������ ���������
  this.toolTipWidth       = 350;
  this.toolTipHeight      = 150;
  // ������ � ����������
  this.STR_HINT           = '';
  // ����� ���� ��������� � ������� �����.�����.���������
  this.AJAX_PROC          = '';
  // ��������� ���������� ��������� (������������� ������)
  this.AJAX_PAR;

  // ��������� ����� �����������
  this.SHOW_TIME        = 2000;
  // ��������� ����� ��������
  this.SHOW_DELAY       = 2000;
  // ��������� ����� �������� ��� �����
  this.AJAX_DELAY       = 0; //1000;
  // �������� ����� (��� ���� ���������)
  this.SCHEME_OWNER     = '';
  
  // ����� ��������� �������
  this.startResize       = false;
  this.startMove         = false;
  
  // ��������� �������� ������ � ������� �������
  this.startHeight       = 0;
  this.startWidth        = 0;
  this.startX            = 0;
  this.startY            = 0;
  // ��������� �������� ������� ���� ��� ��������� �������
  this.resizeXBase       = 0;
  this.resizeYBase       = 0;
  // �������� ����������
  this.FADE_TIME         = 400;
  // ������������� ���������, ���������� � ������������
  if (array){
    for(i in array){
      this[i]=array[i];
    }
  }
  
  this.changeName=function(newName){
    var re= new RegExp(GLOBAL_THIS.VAR_NAME+'\.',"g");
    // zlo o_O
    GLOBAL_THIS.divToolTip.html(GLOBAL_THIS.divToolTip.html().replace(re,newName+'.'));
    GLOBAL_THIS.VAR_NAME=newName;
  }
  
  
  this.l_freeze_up=function(obj,ev){
    obj.src="/"+GLOBAL.GLB_ICO_DIR+"/tooltip/pin_yellow."+GLOBAL.GLB_EXT
    obj.title="���������"
    var i=freezedObjects.indexOf(GLOBAL_THIS)+1
    if (i==0){
      i=freezedObjects.push(new ToolTip(GLOBAL_THIS))
      GLOBAL_THIS.divToolTip=null
      freezedObjects[i-1].GLOBAL_THIS=freezedObjects[i-1]
      freezedObjects[i-1].changeName('freezedObjects['+(i-1)+']')
      freezedObjects[i-1].divToolTipScroll=$('.scrollableDiv',freezedObjects[i-1].divToolTip)
      freezedObjects[i-1].divToolTipInner=$('.divToolTipInner',freezedObjects[i-1].divToolTipScroll)
      freezedObjects[i-1].divToolTip.mouseover(freezedObjects[i-1].setMouseInDiv)
      freezedObjects[i-1].divToolTip.mouseout(freezedObjects[i-1].unSetMouseInDiv)
    }
    GLOBAL_THIS.isShownTip=false
    clearInterval(GLOBAL_THIS.hideInterval)
    GLOBAL_THIS.hideInterval=null
    freezedObjects[i-1].freeze=freezedObjects[i-1].l_freeze_down
    ev.cancelBubble=true
    ev.returnValue=false
    return false

  }
  
  this.l_freeze_down=function(obj,ev){
    obj.src="/"+GLOBAL.GLB_ICO_DIR+'/tooltip/pin_grey.'+GLOBAL.GLB_EXT
    obj.title="���������"
    GLOBAL_THIS.hideInterval=setInterval(function(){GLOBAL_THIS.hideTooltip(0)},GLOBAL_THIS.SHOW_TIME)
    GLOBAL_THIS.isShownTip=true
    GLOBAL_THIS.freeze=GLOBAL_THIS.l_freeze_up
    ev.cancelBubble=true
    return false
  }
  
  this.freeze=function(obj,ev){
    GLOBAL_THIS.l_freeze_up(obj,ev)
  }
  
  // ����� ����� � �������
  this.setMouseInDiv=function(){
    GLOBAL_THIS.isMouseInDiv=true
  }
  // ����� ����� �� �������
  this.unSetMouseInDiv=function(){
    GLOBAL_THIS.isMouseInDiv=false
  }
  // ����������� ������ ��������� �������
  this.registerMove=function(e,isMove){
    e.preventDefault&&e.preventDefault();
    GLOBAL_THIS.unRegisterMove(e)
    if (!isMove){
      document.body.style.cursor='se-resize'
      GLOBAL_THIS.startResize=true
      GLOBAL_THIS.startHeight=GLOBAL_THIS.divToolTipScroll[0].clientHeight
      GLOBAL_THIS.startWidth=GLOBAL_THIS.divToolTipScroll[0].clientWidth
    } else {
      document.body.style.cursor='move' 
      GLOBAL_THIS.startMove=true
      GLOBAL_THIS.startX=(/(\d*)/.exec(GLOBAL_THIS.divToolTip.css("left")))[0]
      GLOBAL_THIS.startY=(/(\d*)/.exec(GLOBAL_THIS.divToolTip.css("top")))[0]
      //alert(GLOBAL_THIS.startX+'\n'+GLOBAL_THIS.startY)
    }
    GLOBAL_THIS.resizeYBase=(e.clientY||e.Y)
    GLOBAL_THIS.resizeXBase=(e.clientX||e.X)
    $('body').bind("mousemove",function(ev){GLOBAL_THIS.makeMove(ev)})
    $('body').bind("mouseup",function(ev){GLOBAL_THIS.unRegisterMove(ev)})
    if ($.browser.msie){
      //ppc! 
      document.onselectstart = function() {return false}
      e.returnValue=false
      window.event.returnValue=false
      //window.event=null
      return false
    }
  }
  // ������ ����������� ��������� �������
  this.unRegisterMove=function(e){
    document.body.style.cursor='default' 
    if (GLOBAL_THIS.startResize){
      if ($.browser.msie){
        document.onselectstart = null
      }
      $('body').unbind("mousemove",function(ev){GLOBAL_THIS.makeMove(ev)})
      $('body').unbind("mouseup",function(ev){GLOBAL_THIS.unRegisterMove(ev)})
      GLOBAL_THIS.startResize=false
    }
    if (GLOBAL_THIS.startMove){
      if ($.browser.msie){
        document.onselectstart = null
      }
      $('body').unbind("mousemove",function(ev){GLOBAL_THIS.makeMove(ev)})
      $('body').unbind("mouseup",function(ev){GLOBAL_THIS.unRegisterMove(ev)})
      GLOBAL_THIS.startMove=false
    }
  }
  // ����������� �������� ����� �� ��������� �������
  this.makeMove=function (e){
    if (GLOBAL_THIS.startResize){
      var xlen=GLOBAL_THIS.startWidth+(e.clientX||e.X)-GLOBAL_THIS.resizeXBase
      var ylen=GLOBAL_THIS.startHeight+(e.clientY||e.Y)-GLOBAL_THIS.resizeYBase
      ylen=(ylen<40)?40:ylen
      xlen=(xlen<40)?40:xlen
      GLOBAL_THIS.divToolTipScroll.css('height',ylen)
      GLOBAL_THIS.divToolTipScroll.css('width',xlen)
      GLOBAL_THIS.toolTipWidth=xlen
      GLOBAL_THIS.toolTipHeight=ylen
    }
    if (GLOBAL_THIS.startMove){
      var xlen=GLOBAL_THIS.startX-0+(e.clientX||e.X)-GLOBAL_THIS.resizeXBase
      var ylen=GLOBAL_THIS.startY-0+(e.clientY||e.Y)-GLOBAL_THIS.resizeYBase
      GLOBAL_THIS.divToolTip.css('left',xlen)
      GLOBAL_THIS.divToolTip.css('top',ylen)
    }
    e.returnValue=false
    return false
  }

  /*
   * ������� �������
   */
  this.hideTooltip=function(force){
    if (((!GLOBAL_THIS.isMouseInDiv)&&(!GLOBAL_THIS.startResize))||(force)){
      /*
       *  ���� ����� �� � �������, ��� �����������, �� ��������
       */
      GLOBAL_THIS.divToolTip.hide()
      GLOBAL_THIS.isShownTip=false
      clearInterval(GLOBAL_THIS.hideInterval)
      GLOBAL_THIS.hideInterval=null
    }
  }

  /*
   *  ��������� ���������� ��� ��������
   */
  this.ToolTipOver=function(obj,e,additParam,force){
    GLOBAL_THIS.xpos=(e.clientX||e.x)+document.body.scrollLeft
    GLOBAL_THIS.ypos=(e.clientY||e.y)+document.body.scrollTop
    GLOBAL_THIS.ypos=(e.clientY||e.y)+document.body.scrollTop
    var count=++GLOBAL_THIS.cnt
    GLOBAL_THIS.activeObject=obj
    /*
     *  �������������� �������� ���������
     */
    if (additParam){
      /*
       *  ��� ��������� "$cTest string""
       */
      if (additParam.indexOf('$c')==0){
        GLOBAL_THIS.STR_HINT=additParam.substr(2)
        if (GLOBAL_THIS.activeObject!=GLOBAL_THIS.prevActiveObject){
          GLOBAL_THIS.prevActiveObject=GLOBAL_THIS.activeObject
          var tt=setTimeout(function(){GLOBAL_THIS.showToolTip(obj,e,count)},GLOBAL_THIS.SHOW_DELAY);
          timeOutString=":"+tt
        }
      }

      /*
       *  ��� ������ "$i345"
       */
      if (additParam.indexOf('$i')==0){
        GLOBAL_THIS.STR_HINT=this.indexes[additParam.substr(2)]
        //if (GLOBAL_THIS.activeObject!=GLOBAL_THIS.prevActiveObject){
          GLOBAL_THIS.prevActiveObject=GLOBAL_THIS.activeObject
          var tt=setTimeout(function(){GLOBAL_THIS.showToolTip(obj,e,count)},GLOBAL_THIS.SHOW_DELAY);
          timeOutString=":"+tt
        //}
      }
      
      /*
       *  ��� ������ "$pAPXP_HINT.APX_CARD_HINT;P_ID=53858700""
       */
      if (additParam.indexOf('$p')==0){
        var arr=additParam.split(';')
        if (arr.length!=0){
          GLOBAL_THIS.AJAX_PROC=arr[0].substr(2)
          GLOBAL_THIS.AJAX_PAR={}
          for(var i=1;i<arr.length;i++){
            var par_val=arr[i].split('=')
            if (par_val.length>=1){
              if (typeof(GLOBAL_THIS.AJAX_PAR[par_val[0]])=='undefined'){
                GLOBAL_THIS.AJAX_PAR[par_val[0]]=[par_val.slice(1).join('=')]
              }else{
                GLOBAL_THIS.AJAX_PAR[par_val[0]].push(par_val.slice(1).join('='))
              }
            }
          }
        }
        var tt=setTimeout(function(){GLOBAL_THIS.ajaxGetHint(obj,e,count,force)},GLOBAL_THIS.AJAX_DELAY)
        timeOutString=":"+tt
      }
      /*
       *  ��� ������ "$aAPXP_HINT.APX_CARD_HINT?P_ID=53858700""
       */
      if (additParam.indexOf('$a')==0){
        var tt=setTimeout(function(){GLOBAL_THIS.ajaxGetHintURL(additParam.substr(2),obj,e,count,force)},GLOBAL_THIS.AJAX_DELAY)
        timeOutString=":"+tt
      }
    } else {
      if (GLOBAL_THIS.activeObject!=GLOBAL_THIS.prevActiveObject){
        GLOBAL_THIS.prevActiveObject=GLOBAL_THIS.activeObject
        var tt=setTimeout(function(){GLOBAL_THIS.showToolTip(obj,e,count,force)},GLOBAL_THIS.SHOW_DELAY)
        timeOutString=":"+tt
      }
    }
  }
  this.startShow=this.ToolTipOver
  
  // ��������� ������ �������� ���������
  this.ajaxGetHint=function (obj,e,counter,force){
    if (!GLOBAL_THIS.enableToolTips&&!force) return
    /*
     *  ���� ��� ������������
     */
    if (GLOBAL_THIS.isShownTip) return
    /*
     *  �� ��������� �������� ������
     */
    if (!GLOBAL_THIS.activeObject) return
    /*
     *  �������� �� ���
     */
    if (GLOBAL_THIS.activeObject!=obj) return
    if (counter!=GLOBAL_THIS.cnt) return
    
    $.ajax({
      type: "POST",
      url: (GLOBAL_THIS.SCHEME_OWNER&&(GLOBAL_THIS.SCHEME_OWNER+'.'+GLOBAL_THIS.AJAX_PROC))||(GLOBAL_THIS.AJAX_PROC),
      data: GLOBAL_THIS.AJAX_PAR,
      success: function(data){
        GLOBAL_THIS.STR_HINT=data
        GLOBAL_THIS.showToolTip(obj,e,counter,force)
      }
    })
  }
  // ��������� ������ �������� ���������
  this.ajaxGetHintURL=function (p_url,obj,e,counter,force){
    if (!GLOBAL_THIS.enableToolTips&&!force) return
    /*
     *  ���� ��� ������������
     */
    if (GLOBAL_THIS.isShownTip) return
    /*
     *  �� ��������� �������� ������
     */
    if (!GLOBAL_THIS.activeObject) return
    /*
     *  �������� �� ���
     */
    if (GLOBAL_THIS.activeObject!=obj) return
    if (counter!=GLOBAL_THIS.cnt) return
    var l_url=p_url.split('?')[0]
    var l_data=p_url.split('?').slice(1).join('?');
    $.ajax({
      type: "POST",
      url: l_url,
      data: l_data,
      success: function(data){
        GLOBAL_THIS.STR_HINT=data
        GLOBAL_THIS.showToolTip(obj,e,counter,force)
      }
    })
  }
  // ����� ����� �� ��������
  this.ToolTipOut=function (obj,e){
    GLOBAL_THIS.cnt++
    GLOBAL_THIS.activeObject=null
    if (!GLOBAL_THIS.isShownTip)
      GLOBAL_THIS.prevActiveObject=null
  }
  this.stopShow=this.ToolTipOut
  // ����� ������������ � �������
  this.ToolTipMove=function(obj,e){
    GLOBAL_THIS.xpos=(e.clientX||e.x)+document.body.scrollLeft
    GLOBAL_THIS.ypos=(e.clientY||e.y)+document.body.scrollTop
  }
  this.changeShowPos=this.ToolTipMove
  // ����������/���������� �������
  this.toggleToolTip=function(){
    GLOBAL_THIS.enableToolTips=!GLOBAL_THIS.enableToolTips
  }
  // �������� �������
  this.createToolTip=function(){
    GLOBAL_THIS.divToolTip = $('\
    <div class="toolTip">\
      <table cellpadding="0" cellspacing="0">\
        <tr>\
          <td>\
            <table class="innerTable" cellpadding="0" cellspacing="0">\
              <tr class="trHeader">\
                <td class="tdHeaderLeft" onmousedown="'+GLOBAL_THIS.VAR_NAME+'.registerMove(event,1);"/>\
                <td class="tdHeaderCenter" onmousedown="'+GLOBAL_THIS.VAR_NAME+'.registerMove(event,1);">\
                  <img class="imgFreese" src="/'+GLOBAL.GLB_ICO_DIR+'/tooltip/pin_grey.'+GLOBAL.GLB_EXT+'" title="���������" onmousedown="'+GLOBAL_THIS.VAR_NAME+'.freeze(this,event)"/></td>\
                <td class="tdHeaderRight">\
                  <div onclick="'+GLOBAL_THIS.VAR_NAME+'.hideTooltip(1)" title="�������"/>\
                </td>\
              </tr>\
            </table>\
          </td>\
        </tr>\
        <tr class="trMiddle">\
          <td>\
            <table class="innerTable" cellpadding="0" cellspacing="0">\
              <tr>\
                <td>\
                  <div class="scrollableDiv">\
                    <div class="divToolTipInner">\
                    </div>\
                  </div>\
                </td>\
              </tr>\
            </table>\
          </td>\
        </tr>\
        <tr class="trFooter">\
          <td>\
            <table class="innerTable" cellpadding="0" cellspacing="0">\
              <tr>\
                <td class="tdFooterCenter">\
                  <input type="checkbox" checked="checked" onclick="'+GLOBAL_THIS.VAR_NAME+'.toggleToolTip()">'+GLOBAL_MSG.get("show")+'</input>\
                </td>\
                <td class="tdFooterRight">\
                  <div onmousedown="'+GLOBAL_THIS.VAR_NAME+'.registerMove(event);"/>\
                </td>\
              </tr>\
            </table>\
          </td>\
        </tr>\
      </table>\
    </div>\
    ')
    GLOBAL_THIS.divToolTip.css('display','none')
    GLOBAL_THIS.divToolTipScroll=$('.scrollableDiv',GLOBAL_THIS.divToolTip)
    GLOBAL_THIS.divToolTipInner=$('.divToolTipInner',GLOBAL_THIS.divToolTipScroll)
    GLOBAL_THIS.divToolTip.appendTo($('form'))
    GLOBAL_THIS.divToolTip.mouseover(GLOBAL_THIS.setMouseInDiv)
    GLOBAL_THIS.divToolTip.mouseout(GLOBAL_THIS.unSetMouseInDiv)
  }
  // ����������� �������
  this.showToolTip=function(obj,e,counter,force){
    if (!GLOBAL_THIS.enableToolTips&&!force) return
    /*
     *  ��������
     */
    if (!GLOBAL_THIS.divToolTip){
      GLOBAL_THIS.createToolTip()
    }
    
    /*
     *  ���� ��� ������������
     */
    if (GLOBAL_THIS.isShownTip) return
    
    /*
     *  �� ��������� �������� ������
     */
    if (!GLOBAL_THIS.activeObject) return
    
    /*
     *  �������� �� ���
     */
    if (GLOBAL_THIS.activeObject!=obj) return

    if (counter!=GLOBAL_THIS.cnt) return
    /*
     *  ���������� �������
     */
    if (GLOBAL_THIS.STR_HINT){
      GLOBAL_THIS.divToolTipInner.html(GLOBAL_THIS.STR_HINT)
      GLOBAL_THIS.STR_HINT=''
    } else {
      GLOBAL_THIS.divToolTipInner.html(GLOBAL_THIS.activeObject.value.replace(/::/g,'<hr/>'))
    }
    
    if (!GLOBAL_THIS.divToolTipInner.html()) return
    GLOBAL_THIS.isShownTip=true
    /*
     *  ���������� ������� �����������
     */
    
    GLOBAL_THIS.divToolTipScroll.css("width",GLOBAL_THIS.toolTipWidth)
    GLOBAL_THIS.divToolTipScroll.css("height",GLOBAL_THIS.toolTipHeight)

    GLOBAL_THIS.divToolTip.css(
        'left'
      , (GLOBAL_THIS.xpos+GLOBAL_THIS.toolTipWidth+20<document.body.clientWidth)?(GLOBAL_THIS.xpos):(GLOBAL_THIS.xpos-GLOBAL_THIS.toolTipWidth-20)
    )
    
    GLOBAL_THIS.divToolTip.css(
        'top'
      , (GLOBAL_THIS.ypos+GLOBAL_THIS.toolTipHeight+20<document.body.clientHeight)?(GLOBAL_THIS.ypos):(GLOBAL_THIS.ypos-GLOBAL_THIS.toolTipHeight-20)
    )
    /*
     *  ����������� ���������
     */
    GLOBAL_THIS.divToolTip.fadeIn(GLOBAL_THIS.FADE_TIME)
    /*
     *  ������ ������� ���������
     */
    GLOBAL_THIS.hideInterval=setInterval(function(){GLOBAL_THIS.hideTooltip(0)},GLOBAL_THIS.SHOW_TIME)
  }
}

var toolTip=new ToolTip();

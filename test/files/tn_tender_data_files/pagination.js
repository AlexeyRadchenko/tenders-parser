
function goToPagination(p_region,params){
    if ((params)&&(params.indexOf('current')!=-1)) return
    //~ if (GLOBAL.APP_USER=='L002_ZEN'){
      //~ var strToObj=function(p_str){
        //~ var l_arr=p_str.split('&');
        //~ var l_obj={}
        //~ for(var i=0;i<l_arr.length;i++){
            //~ var t =l_arr[i].split('=')
            //~ l_obj[t[0]]=t[1]
        //~ }
        //~ return l_obj;
      //~ }
      //~ Report.customize.loadRegion({
          //~ real_id   :p_region
        //~ , urlParam: strToObj(params)
        //~ , request :"pg_R_"+p_region
      //~ });
      //~ return;
    //~ }
    window.location=Report.customize.rid[p_region].pagination+params;
    return;
    var address=window.location
    /*get "p" parameter*/
    var url=/\?p=([^&]*)/.exec(address)[1]
    var col_values=url.split(':')
    if (p_region){
      /*0=App:1=Page:2=Session:3=Request:4=Debug:5=ClearCache:6=itemNames:7=itemValues:8=PrinterFriendly*/
      window.location="f?p="+col_values[0]+
                      ":"+col_values[1]+
                      ":"+col_values[2]+
                      ":"+"pg_R_"+p_region+
                      ":"+(col_values[4]||"")+
                      ":"+""+
                      ":"+(col_values[6]||"")+
                      ":"+(col_values[7]||"")+
                      ":"+(col_values[8]||"")+params
    } else {
      window.location="f?p="+col_values[0]+
                ":"+col_values[1]+
                ":"+col_values[2]+
                ":"+""+
                ":"+(col_values[4]||"")+
                ":"+"RP"+
                ":"+(col_values[6]||"")+
                ":"+(col_values[7]||"")+
                ":"+(col_values[8]||"")
    }
}

function changeAhref(a_obj){
  
  var region      = /pg_R_(\d*)/.exec(a_obj.href)
  var min_r       = /pg_min_row=(\d*)/.exec(a_obj.href)
  var max_r       = /pg_max_rows=(\d*)/.exec(a_obj.href)
  var fetch       = /pg_rows_fetched=(\d*)/.exec(a_obj.href)
  try{
    return "javascript:goToPagination('"+region[1]+"','&pg_min_row="+min_r[1]+"&pg_max_rows="+max_r[1]+"&pg_rows_fetched="+fetch[1]+"')"
  }catch (e){
    return
  }
}

function processPagination(context){
      var pag=$('.pagination',context).each(
      function(){
        var a_=$('a',this);
        var sel_=$('select',this);
        for(var i=0;i<a_.size();i++){
          a_[i].href=changeAhref(a_[i]);
        }
        for(var i=0;i<sel_.size();i++){
          var region = sel_.attr('id').substr(4);/*var region = /pg_R_(\d*)/.exec(sel_[i].onchange)*/
          var fetch  = '100';/*/pg_rows_fetched=(\d*)/.exec(sel_[i].onchange)*/
          $('option',sel_[i]).each(
            function(){
              this.innerHTML=this.innerHTML.replace('of','из')
              this.innerHTML=this.innerHTML.replace('row(s)','строк(и)')
              this.innerHTML=this.innerHTML.replace('more','более')
              this.innerHTML=this.innerHTML.replace('than','чем')
            }
          )
          
          sel_[i].onchange=function(){
            goToPagination(
                region
              , '&pg_min_row='+this.options[this.selectedIndex].value+'&pg_rows_fetched='+fetch
			//зачем нужно кол-во в фетче знать я не разобрался, вроде и так роботает
            )
          }
          
        }
      }
    )
    var tables=$('table[summary=pagination]',context)
    
    tables.find('a').each(
      function(){
        if (this.href.indexOf('javascript:goToPagination')==-1){
          var region=$(this).parents('div').eq(0).children().eq(0).attr('class').substr(8);
          // for Standard APEX regions
          if (!region) {region=$(this).parents('table[region_id]').eq(0).attr('region_id').substr(1);}
          this.parentNode.innerHTML = 'Количество строк меньше чем запрашивается'
          +'<br/><a href="javascript:goToPagination(\''+region+'\',\'\')">Перейти к началу таблицы</a>';
        }
      }
    )
    
    tables.show()
}


$(document).ready(function(){
    processPagination($('body'));
  }
)

(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-93404924"],{"02a6":function(t,s,a){"use strict";a("939c")},"2e90":function(t,s,a){"use strict";var e=function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"list_wrap"},t._l(t.itemData,(function(t,s){return a("Item",{key:s,attrs:{inx:s,id:t.id,type:t.type,status:t.status_code,itemName:t.firmware_name,time:t.created_at}})})),1)},n=[],i=function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"item_box"},[a("h5",{staticClass:"title"},[a("i",{staticClass:"icon"}),a("span",{attrs:{title:t.itemName}},[t._v(t._s(t.itemName))])]),a("dl",[a("dt",[t._v("解压时间:")]),a("dd",[t._v(t._s(t._f("timeFilter")(t.time)))])]),a("div",{staticClass:"status_box"},["extract"===t.type||"completed_unpack"===t.type||"simulation_unpack"===t.type?a("div",{staticClass:"status_unpack"},[a("div",{directives:[{name:"show",rawName:"v-show",value:1==t.status,expression:"status == 1"}],staticClass:"status_1"},[t._v("解压成功")]),a("div",{directives:[{name:"show",rawName:"v-show",value:2==t.status,expression:"status == 2"}],staticClass:"status_2"},[t._v("解压失败")]),a("div",{directives:[{name:"show",rawName:"v-show",value:3==t.status,expression:"status == 3"}],staticClass:"status_3"},[t._v("解压中")])]):"analysis"===t.type?a("div",{staticClass:"status_analysis"},[a("div",{directives:[{name:"show",rawName:"v-show",value:1==t.status,expression:"status == 1"}],staticClass:"status_1"},[t._v("分析完成")]),a("div",{directives:[{name:"show",rawName:"v-show",value:2==t.status,expression:"status == 2"}],staticClass:"status_2"},[t._v("分析失败")]),a("div",{directives:[{name:"show",rawName:"v-show",value:3==t.status,expression:"status == 3"}],staticClass:"status_3"},[t._v("分析中")])]):"detection"===t.type?a("div",{staticClass:"status_detection"},[a("div",{directives:[{name:"show",rawName:"v-show",value:1==t.status,expression:"status == 1"}],staticClass:"status_1"},[t._v("检测完成")]),a("div",{directives:[{name:"show",rawName:"v-show",value:2==t.status,expression:"status == 2"}],staticClass:"status_2"},[t._v("检测失败")]),a("div",{directives:[{name:"show",rawName:"v-show",value:3==t.status,expression:"status == 3"}],staticClass:"status_3"},[t._v("检测中")])]):"simulation"===t.type?a("div",{staticClass:"status_simulation"},[a("div",{directives:[{name:"show",rawName:"v-show",value:1==t.status,expression:"status == 1"}],staticClass:"status_1"},[t._v("仿真成功")]),a("div",{directives:[{name:"show",rawName:"v-show",value:2==t.status,expression:"status == 2"}],staticClass:"status_2"},[t._v("仿真失败")]),a("div",{directives:[{name:"show",rawName:"v-show",value:3==t.status,expression:"status == 3"}],staticClass:"status_3"},[t._v("仿真中")])]):t._e()]),a("ButtonGroup",{attrs:{type:t.type,id:t.id,inx:t.inx,status:t.status}})],1)},u=[],o=(a("ac1f"),a("5319"),function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("div",{staticClass:"btn_group"},[a("div",{directives:[{name:"show",rawName:"v-show",value:"extract"===t.type,expression:"type === 'extract'"}],staticClass:"btn_box"},[1==t.status?a("button",{staticClass:"btn1",on:{click:function(s){return t.downLoadfile(t.id)}}},[t._v("下载")]):2==t.status?a("button",{staticClass:"btn1"},[t._v("重新解压")]):3==t.status?a("button",{staticClass:"btn1-not"},[t._v("下载")]):t._e(),1==t.status||2==t.status?a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTask(t.id)}}},[t._v("删除")]):3==t.status?a("button",{staticClass:"btn2-not"},[t._v("删除")]):t._e()]),a("div",{directives:[{name:"show",rawName:"v-show",value:"analysis"===t.type,expression:"type === 'analysis'"}],staticClass:"btn_box"},[1==t.status?a("button",{staticClass:"btn1",on:{click:function(s){return t.toDetail(t.id)}}},[t._v("查看")]):t._e(),2==t.status?a("button",{staticClass:"btn1"},[t._v("重新分析")]):3==t.status?a("button",{staticClass:"btn1-not"},[t._v("查看")]):t._e(),1==t.status||2==t.status?a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTask(t.id)}}},[t._v("删除")]):3==t.status?a("button",{staticClass:"btn2-not"},[t._v("删除")]):t._e()]),a("div",{directives:[{name:"show",rawName:"v-show",value:"detection"===t.type,expression:"type === 'detection'"}],staticClass:"btn_box"},[1==t.status?a("button",{staticClass:"btn1",on:{click:function(s){return t.toDetail(t.id)}}},[t._v("查看")]):2==t.status?a("button",{staticClass:"btn1"},[t._v("重新检测")]):3==t.status?a("button",{staticClass:"btn1-not"},[t._v("查看")]):t._e(),1==t.status||2==t.status?a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTask(t.id)}}},[t._v("删除")]):3==t.status?a("button",{staticClass:"btn2-not"},[t._v("删除")]):t._e()]),a("div",{directives:[{name:"show",rawName:"v-show",value:"simulation"===t.type,expression:"type === 'simulation'"}],staticClass:"btn_box"},[1==t.status?a("button",{staticClass:"btn1",on:{click:function(s){return t.toUrl(t.inx)}}},[t._v("查看")]):2==t.status?a("button",{staticClass:"btn1"},[t._v("重新仿真")]):3==t.status?a("button",{staticClass:"btn1-not"},[t._v("查看")]):t._e(),1==t.status||2==t.status?a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTask(t.id)}}},[t._v("删除")]):3==t.status?a("button",{staticClass:"btn2-not"},[t._v("删除")]):t._e()]),a("div",{directives:[{name:"show",rawName:"v-show",value:"completed_unpack"===t.type,expression:"type === 'completed_unpack'"}],staticClass:"btn_box"},[a("button",{staticClass:"btn1",on:{click:function(s){return t.analysis(t.id)}}},[t._v("分析")]),a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTaskUnpack(t.id)}}},[t._v("删除")])]),a("div",{directives:[{name:"show",rawName:"v-show",value:"simulation_unpack"===t.type,expression:"type === 'simulation_unpack'"}],staticClass:"btn_box"},[a("button",{staticClass:"btn1",on:{click:function(s){return t.simulation(t.id)}}},[t._v("开始仿真")]),a("button",{staticClass:"btn2",on:{click:function(s){return t.deleteTaskUnpack(t.id)}}},[t._v("删除")])])])}),c=[],r={name:"Item",props:["id","inx","type","status"],data:function(){return{}},created:function(){},methods:{retry:function(t){this.$parent.$parent.$parent.restart(t)},downLoadfile:function(t){window.open(window.location.origin+"/api/extract/download-extracted-firmware/"+t)},deleteTask:function(t){this.$parent.$parent.$parent.handleDelete(t)},toDetail:function(t){this.$parent.$parent.$parent.toDetail(t)},toUrl:function(t){this.$parent.$parent.$parent.toDetail(t)},deleteTaskUnpack:function(t){this.$parent.$parent.$parent.handleDelete_unpack(t)},analysis:function(t){this.$parent.$parent.$parent.handleAnalysis(t)},simulation:function(t){this.$parent.$parent.$parent.handleSimulation(t)}}},l=r,v=(a("6b3b"),a("2877")),d=Object(v["a"])(l,o,c,!1,null,"118afcc8",null),p=d.exports,_={name:"Item",components:{ButtonGroup:p},props:["id","inx","time","type","status","itemName"],data:function(){return{}},created:function(){},methods:{},watch:{type:{handler:function(){},deep:!0}},filters:{timeFilter:function(t){return t=t.replace("T"," "),t.substring(0,19)}}},m=_,b=(a("02a6"),Object(v["a"])(m,i,u,!1,null,"288cfc3c",null)),w=b.exports,h={name:"FirmwareUnpack",props:["list"],components:{Item:w},data:function(){return{itemData:[]}},created:function(){},methods:{},watch:{list:{handler:function(t){this.itemData=t},deep:!0}}},f=h,C=(a("5fa1"),Object(v["a"])(f,e,n,!1,null,"1fd27a1c",null));s["a"]=C.exports},"5fa1":function(t,s,a){"use strict";a("87c8")},"6b3b":function(t,s,a){"use strict";a("a1a3")},"87c8":function(t,s,a){},"939c":function(t,s,a){},a1a3:function(t,s,a){}}]);
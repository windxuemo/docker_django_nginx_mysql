(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6f28c822"],{2193:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"box"},[a("button",{on:{click:function(e){return t.handle_upload()}}},[t._v("上传固件")]),a("div",{staticClass:"list_box"},[a("List",{attrs:{list:t.list}}),a("el-pagination",{attrs:{background:"",layout:"prev, pager, next,total",total:t.total,"page-size":t.items_per_page,"current-page":t.page},on:{"current-change":t.handleCurrentChange}})],1),a("Upload",{directives:[{name:"show",rawName:"v-show",value:t.upload,expression:"upload"}]}),a("div",{directives:[{name:"show",rawName:"v-show",value:t.delete_item,expression:"delete_item"}],staticClass:"delete_wrap"},[a("div",{staticClass:"delete_box"},[a("i",{staticClass:"close",on:{click:t.close}}),a("h5",[t._v("删除")]),a("p",[t._v("确定要删除本条数据吗？")]),a("div",{staticClass:"button_box"},[a("button",{on:{click:t.confirm}},[t._v("确定")]),a("button",{on:{click:t.close}},[t._v("取消")])])])]),a("div",{staticClass:"foot_box"})],1)},i=[],n=(a("d3b7"),a("159b"),a("2e90")),o=a("d443"),c={name:"FirmwareUnpack",components:{List:n["a"],Upload:o["a"]},data:function(){return{id:"",list:[],total:0,page:1,items_per_page:12,upload:!1,delete_item:!1}},created:function(){this.getList()},methods:{getList:function(){var t=this,e={page:this.page,items_per_page:this.items_per_page};this.$FunctionDetection.getFunctionList(e).then((function(e){200===e.status&&e.data&&(t.list=e.data.tasks,t.total=e.data.total_items,t.list.forEach((function(t){t.type="detection",t.firmware_name=t.binary_name,"completed"===t.status?t.status_code="1":"Pending"===t.status?t.status_code="3":t.status_code="2"})))}))},handle_upload:function(){this.upload=!0},cancel:function(){this.upload=!1},uploads:function(t){var e=this,a=new FormData;a.append("binary_file",t),this.$FunctionDetection.createFunction(a).then((function(t){if(200!==t.status||"任务已创建"!==t.data.message)return e.$message({type:"warning",message:t.data.message});e.upload=!1,e.getList()}))},handleDelete:function(t){this.delete_item=!0,this.id=t},close:function(){this.getList(),this.delete_item=!1},confirm:function(){var t=this;this.$FunctionDetection.deleteFunction(this.id).then((function(e){200===e.status&&(t.$message({type:"success",message:e.data.message}),t.close())}))},handleCurrentChange:function(t){this.page=t,this.getList()},toDetail:function(t){this.$router.push({path:"/detectionDetail",query:{id:t}})}}},u=c,l=(a("85a8"),a("f69c"),a("2877")),d=Object(l["a"])(u,s,i,!1,null,"08823c4d",null);e["default"]=d.exports},"5d7a":function(t,e,a){},"85a8":function(t,e,a){"use strict";a("5d7a")},df1b:function(t,e,a){},f69c:function(t,e,a){"use strict";a("df1b")}}]);
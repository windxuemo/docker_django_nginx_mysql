(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1ae1afdb"],{"0dc8":function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"box"},[1==t.tab_index?a("div",{staticClass:"analy"},[a("button",{on:{click:function(e){return t.handle_upload()}}},[t._v("上传固件")]),a("div",{staticClass:"list_box"},[a("List",{attrs:{list:t.list}}),a("el-pagination",{attrs:{background:"",layout:"prev, pager, next,total",total:t.total,"page-size":t.items_per_page,"current-page":t.page},on:{"current-change":t.handleCurrentChange}})],1),a("Upload",{directives:[{name:"show",rawName:"v-show",value:t.upload,expression:"upload"}]}),a("div",{directives:[{name:"show",rawName:"v-show",value:t.delete_item,expression:"delete_item"}],staticClass:"delete_wrap"},[a("div",{staticClass:"delete_box"},[a("i",{staticClass:"close",on:{click:t.close}}),a("h5",[t._v(t._s(t.tip.title))]),a("p",[t._v(t._s(t.tip.msg))]),a("div",{staticClass:"button_box"},[a("button",{on:{click:t.confirm}},[t._v("确定")]),a("button",{on:{click:t.close}},[t._v("取消")])])])])],1):t._e(),2==t.tab_index?a("div",{staticClass:"unpack"},[a("div",{staticClass:"list_box"},[a("List",{attrs:{list:t.list_unpack}}),a("el-pagination",{attrs:{background:"",layout:"prev, pager, next,total",total:t.total_unpack,"page-size":t.items_per_page,"current-page":t.page_unpack},on:{"current-change":t.handleCurrentChange_unpack}})],1),a("div",{directives:[{name:"show",rawName:"v-show",value:t.delete_item_unpack,expression:"delete_item_unpack"}],staticClass:"delete_wrap"},[a("div",{staticClass:"delete_box"},[a("i",{staticClass:"close",on:{click:t.close}}),a("h5",[t._v(t._s(t.tip.title))]),a("p",[t._v(t._s(t.tip.msg))]),a("div",{staticClass:"button_box"},["delete"===t.handle_type_unpack?a("button",{on:{click:t.confirm_delete_unpack}},[t._v("确定")]):t._e(),"start"===t.handle_type_unpack?a("button",{on:{click:t.confirm_start_unpack}},[t._v("确定")]):t._e(),a("button",{on:{click:t.close_unpack}},[t._v("取消")])])])])]):t._e(),a("div",{staticClass:"foot_box"},[a("div",{staticClass:"btn-left",class:{active:1===t.tab_index},on:{click:function(e){return t.handleTab(1)}}},[t._v("静态分析")]),a("div",{staticClass:"btn-right",class:{active:2===t.tab_index},on:{click:function(e){return t.handleTab(2)}}},[t._v("已解压固件")])])])},i=[],n=(a("d3b7"),a("159b"),a("2e90")),c=a("d443"),l={name:"FirmwareUnpack",components:{List:n["a"],Upload:c["a"]},data:function(){return{tab_index:1,tip:{title:"",msg:""},id:"",list:[],total:0,page:1,items_per_page:12,upload:!1,delete_item:!1,handle_type:"",id_unpack:"",list_unpack:[],total_unpack:0,page_unpack:1,handle_type_unpack:"",delete_item_unpack:!1}},created:function(){this.getList(),this.getList_unpack()},methods:{handleTab:function(t){this.tab_index=t},getList:function(){var t=this,e={page:this.page,items_per_page:this.items_per_page};this.$Analysis.getAnalysisList(e).then((function(e){200===e.status&&e.data&&(t.list=e.data.tasks,t.total=e.data.total_items,t.list.forEach((function(t){t.type="analysis","completed"===t.status?t.status_code="1":"analyzing"===t.status?t.status_code="3":t.status_code="2"})))}))},handle_upload:function(){this.upload=!0},cancel:function(){this.upload=!1},uploads:function(t){var e=this,a=new FormData;a.append("zip_file",t),this.$Analysis.createAnalysis(a).then((function(t){if(200!==t.status||"任务已创建"!==t.data.message)return e.$message({type:"warning",message:t.data.message});e.upload=!1,e.getList()}))},handleDelete:function(t){this.handle_type_unpack="delete",this.tip.title="删除",this.tip.msg="确定要删除本条信息吗？",this.delete_item=!0,this.id=t},close:function(){this.delete_item=!1,this.getList()},confirm:function(){var t=this;this.$Analysis.deleteAnalysis(this.id).then((function(e){200===e.status&&(t.$message({type:"success",message:e.data.message}),t.close())}))},handleCurrentChange:function(t){this.page=t,this.getList()},toDetail:function(t){this.$router.push({path:"/analysisDetail",query:{id:t}})},getList_unpack:function(){var t=this,e={page_unpack:this.page,items_per_page:this.items_per_page};this.$Extract.getCompletedExtractList(e).then((function(e){200===e.status&&e.data&&(t.list_unpack=e.data.tasks,t.total_unpack=e.data.total_items,t.list_unpack.forEach((function(t){t.type="completed_unpack","completed"===t.status&&(t.status_code="1")})))}))},close_unpack:function(){this.delete_item_unpack=!1,this.getList_unpack()},handleDelete_unpack:function(t){this.handle_type_unpack="delete",this.tip.title="删除",this.tip.msg="确定要删除本条信息吗？",this.delete_item_unpack=!0,this.id_unpack=t},confirm_delete_unpack:function(){var t=this;this.$Extract.deleteExtract(this.id_unpack).then((function(e){200===e.status&&(t.$message({type:"success",message:e.data.message}),t.close())}))},handleAnalysis:function(t){this.handle_type_unpack="start",this.tip.title="开始分析",this.tip.msg="确定要开始执行分析吗？",this.delete_item_unpack=!0,this.id_unpack=t},confirm_start_unpack:function(){var t=this,e=new FormData;e.append("task_id",this.id_unpack),this.$Analysis.startAnalysis(e).then((function(e){if(200!==e.status||"任务已创建"!==e.data.message)return t.$message({type:"warning",message:e.data.message});t.delete_item_unpack=!1,t.tab_index=1,t.getList()}))},handleCurrentChange_unpack:function(t){this.page_unpack=t,this.getList_unpack()}}},u=l,o=(a("d504"),a("2877")),p=Object(o["a"])(u,s,i,!1,null,"09d57756",null);e["default"]=p.exports},"4b79":function(t,e,a){},d504:function(t,e,a){"use strict";a("4b79")}}]);
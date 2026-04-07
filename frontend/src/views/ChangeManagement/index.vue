<template>
  <div class="change-management">
    <el-card>
      <template #header>
        <div class="header-actions">
          <span class="title">变更管理</span>
          <el-button type="primary" @click="showCreateDialog">发起变更</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab" type="card" @tab-click="handleTabClick">
        <el-tab-pane label="行动项" name="action_items">
           <div class="tab-filters">
              <span class="label">筛选行动项:</span>
              <el-radio-group v-model="actionFilterStatus" @change="fetchActionData" size="small">
                <el-radio-button label="All">所有行动项</el-radio-button>
                <el-radio-button label="Unfinished">未完成</el-radio-button>
              </el-radio-group>
           </div>

           <el-table :data="actionTableData" style="width: 100%; margin-top:10px;" v-loading="loading" border>
              <el-table-column prop="status" label="状态" width="100">
                  <template #default="scope">
                      <el-tag :type="scope.row.status === 'Done' ? 'success' : 'warning'">{{ scope.row.status === 'Done' ? '已完成' : '待处理' }}</el-tag>
                  </template>
              </el-table-column>
              <el-table-column prop="content" label="行动内容" min-width="200"></el-table-column>
              <el-table-column prop="change_info.code" label="所属变更" width="180">
                  <template #default="scope">
                      <el-link type="primary" @click="showChangeDrawer(scope.row.change_info)">{{ scope.row.change_info.code }}</el-link>
                      <br/>
                      <span style="font-size: 12px; color: #999;">{{ scope.row.change_info.title }}</span>
                  </template>
              </el-table-column>
              <el-table-column prop="owner" label="责任人" width="120"></el-table-column>
              <el-table-column prop="plan_date" label="计划完成时间" width="120" sortable></el-table-column>
              <el-table-column prop="qa_contact" label="跟进人" width="120"></el-table-column>
              <el-table-column prop="completed_at" label="完成时间" width="120"></el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                   <el-button link type="primary" size="small" @click="editActionItem(scope.row)">编辑</el-button>
                   <el-popconfirm title="确定删除吗?" @confirm="deleteAction(scope.row.id)">
                     <template #reference>
                       <el-button link type="danger" size="small">删除</el-button>
                     </template>
                   </el-popconfirm>
                </template>
              </el-table-column>
           </el-table>
        </el-tab-pane>

        <el-tab-pane label="变更流程" name="change_requests">
           <div class="tab-filters">
              <span class="label">筛选流程:</span>
              <el-radio-group v-model="changeFilterStatus" @change="fetchChangeData" size="small">
                <el-radio-button label="All">所有流程</el-radio-button>
                <el-radio-button label="Open">未完成流程</el-radio-button>
              </el-radio-group>
              <el-input
                v-model="searchKeyword"
                placeholder="输入控制号或标题搜索"
                class="custom-search-input"
                @keyup.enter="handleSearch"
                @input="val => !val && handleSearch()"
                clearable
                @clear="handleSearch"
              >
                <template #suffix>
                    <el-icon class="search-icon" @click="handleSearch" style="cursor: pointer;"><Search /></el-icon>
                </template>
              </el-input>
              <el-button type="success" :icon="Download" @click="handleExport" style="margin-left: 10px;">导出Excel</el-button>
           </div>

           <el-table :data="changeTableData" style="width: 100%; margin-top:10px;" v-loading="loading" row-key="id">
            <el-table-column type="expand">
              <template #default="props">
                <div class="detail-container">
                   <el-descriptions title="变更详情" :column="2" border>
                     <el-descriptions-item label="变更描述">{{ props.row.description }}</el-descriptions-item>
                     <el-descriptions-item label="影响评估">{{ props.row.impact_assessment }}</el-descriptions-item>
                     <el-descriptions-item label="批准日期">{{ props.row.approval_date }}</el-descriptions-item>
                     <el-descriptions-item label="关闭日期">{{ props.row.close_date }}</el-descriptions-item>
                     <el-descriptions-item label="CMO同意">{{ props.row.cmo_agreed ? '是' : '否' }}</el-descriptions-item>
                     <el-descriptions-item label="CMO编号">{{ props.row.cio_code }}</el-descriptions-item>
                   </el-descriptions>
                   <div class="action-items-section">
                     <div class="section-header">
                       <h4>行动项摘要</h4>
                       <el-button size="small" type="primary" @click="showAddActionDialog(props.row)">添加行动项</el-button>
                     </div>
                     <el-table :data="props.row.action_items" border size="small">
                        <el-table-column prop="content" label="内容"></el-table-column>
                        <el-table-column prop="owner" label="责任人" width="100"></el-table-column>
                        <el-table-column prop="plan_date" label="计划完成时间" width="120"></el-table-column>
                        <el-table-column prop="completed_at" label="实际完成时间" width="120"></el-table-column>
                        <el-table-column prop="status" label="状态" width="100">
                            <template #default="scope">
                                <el-tag :type="scope.row.status === 'Done' ? 'success' : 'warning'">{{ scope.row.status === 'Done' ? '已完成' : '待处理' }}</el-tag>
                            </template>
                        </el-table-column>
                     </el-table>
                   </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="code" label="变更控制号" width="150" sortable></el-table-column>
            <el-table-column prop="title" label="变更标题" min-width="150"></el-table-column>
            <el-table-column prop="department" label="发起部门" width="120" sortable></el-table-column>
            <el-table-column prop="creator" label="发起人" width="120" sortable></el-table-column>
            <el-table-column prop="created_at" label="发起日期" width="120" sortable></el-table-column>
            <el-table-column prop="level" label="变更级别" width="120" sortable></el-table-column>
            <el-table-column prop="status" label="状态" width="100" sortable>
               <template #default="scope">
                 <el-tag :type="scope.row.status === 'Closed' ? 'success' : 'danger'">{{ scope.row.status === 'Closed' ? '已关闭' : '进行中' }}</el-tag>
               </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="editChange(scope.row)">编辑</el-button>
                <el-popconfirm title="确定删除吗?" @confirm="removeChange(scope.row.id)">
                   <template #reference>
                     <el-button link type="danger" size="small">删除</el-button>
                   </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- Side Drawer for Change Detail -->
    <el-drawer v-model="drawerVisible" title="变更流程详情" size="50%">
        <div v-if="currentChangeInfo" class="drawer-content">
            <h3>{{ currentChangeInfo.title }} ({{ currentChangeInfo.code }})</h3>
            <el-descriptions :column="1" border>
                 <el-descriptions-item label="状态">
                    <el-tag :type="currentChangeInfo.status === 'Closed' ? 'success' : 'danger'">{{ currentChangeInfo.status === 'Closed' ? '已关闭' : '进行中' }}</el-tag>
                 </el-descriptions-item>
                 <el-descriptions-item label="发起部门">{{ currentChangeInfo.department }}</el-descriptions-item>
                 <el-descriptions-item label="发起人">{{ currentChangeInfo.creator }}</el-descriptions-item>
                 <el-descriptions-item label="发起日期">{{ currentChangeInfo.created_at }}</el-descriptions-item>
                 <el-descriptions-item label="变更级别">{{ currentChangeInfo.level }}</el-descriptions-item>
                 <el-descriptions-item label="变更描述">{{ currentChangeInfo.description }}</el-descriptions-item>
                 <el-descriptions-item label="影响评估">{{ currentChangeInfo.impact_assessment }}</el-descriptions-item>
                 <el-descriptions-item label="批准日期">{{ currentChangeInfo.approval_date }}</el-descriptions-item>
                 <el-descriptions-item label="关闭日期">{{ currentChangeInfo.close_date }}</el-descriptions-item>
                 <el-descriptions-item label="CMO同意">{{ currentChangeInfo.cmo_agreed ? '是' : '否' }}</el-descriptions-item>
                 <el-descriptions-item label="CMO编号">{{ currentChangeInfo.cio_code }}</el-descriptions-item>
            </el-descriptions>
            <div style="margin-top: 20px; text-align: center;">
                <el-button type="primary" @click="editChange(currentChangeInfo)">编辑该变更</el-button>
            </div>
        </div>
    </el-drawer>

    <!-- Create/Edit Change Dialog -->
    <el-dialog v-model="changeDialogVisible" :title="isEditChange ? '编辑变更' : '发起变更'" width="60%">
        <el-form :model="changeForm" label-width="120px">
            <el-form-item label="变更控制号" required>
                <el-input v-model="changeForm.code" :disabled="isEditChange"></el-input>
            </el-form-item>
            <el-form-item label="变更标题" required>
                <el-input v-model="changeForm.title"></el-input>
            </el-form-item>
             <el-form-item label="发起人" required>
                <el-input v-model="changeForm.creator" :disabled="isEditChange"></el-input>
            </el-form-item>
            <el-form-item label="发起部门" required>
                <el-input v-model="changeForm.department"></el-input>
            </el-form-item>
             <el-form-item label="发起日期">
                <el-date-picker v-model="changeForm.created_at" type="date" value-format="YYYY-MM-DD" placeholder="默认为今天"></el-date-picker>
            </el-form-item>
             <el-form-item label="变更描述">
                <el-input v-model="changeForm.description" type="textarea" :rows="3"></el-input>
            </el-form-item>
             <el-form-item label="变更级别">
                <el-select v-model="changeForm.level" placeholder="请选择">
                    <el-option label="微小变更" value="微小变更"></el-option>
                    <el-option label="一般变更" value="一般变更"></el-option>
                    <el-option label="重大变更" value="重大变更"></el-option>
                </el-select>
            </el-form-item>
            <template v-if="isEditChange">
                 <el-divider>评估与关闭</el-divider>
                 <el-form-item label="影响评估">
                    <el-input v-model="changeForm.impact_assessment" type="textarea" :autosize="{ minRows: 3 }"></el-input>
                 </el-form-item>
                 <el-form-item label="批准日期">
                    <el-date-picker v-model="changeForm.approval_date" type="date" value-format="YYYY-MM-DD"></el-date-picker>
                 </el-form-item>
                 <el-form-item label="CMO同意">
                    <el-switch v-model="changeForm.cmo_agreed"></el-switch>
                 </el-form-item>
                 <el-form-item label="CMO编号">
                    <el-input v-model="changeForm.cio_code"></el-input>
                 </el-form-item>
                 <el-form-item label="状态">
                    <el-radio-group v-model="changeForm.status">
                        <el-radio label="Open">进行中</el-radio>
                        <el-radio label="Closed">已关闭</el-radio>
                    </el-radio-group>
                 </el-form-item>
                 <el-form-item label="关闭日期" v-if="changeForm.status === 'Closed'">
                    <el-date-picker v-model="changeForm.close_date" type="date" value-format="YYYY-MM-DD"></el-date-picker>
                 </el-form-item>
                 <el-divider>行动项管理</el-divider>
                 <div style="margin-bottom: 10px;">
                    <el-button type="primary" size="small" @click="showAddActionDialog(changeForm)">添加行动项</el-button>
                 </div>
                 <el-table :data="localActionItems" border size="small">
                    <el-table-column prop="content" label="内容"></el-table-column>
                    <el-table-column prop="owner" label="责任人" width="100"></el-table-column>
                    <el-table-column prop="plan_date" label="计划完成时间" width="120"></el-table-column>
                    <el-table-column prop="completed_at" label="实际完成时间" width="120"></el-table-column>
                    <el-table-column prop="status" label="状态" width="100">
                        <template #default="scope">
                            <el-tag :type="scope.row.status === 'Done' ? 'success' : 'warning'">{{ scope.row.status === 'Done' ? '已完成' : '待处理' }}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120">
                        <template #default="scope">
                            <el-button link type="primary" size="small" @click="editActionItem(scope.row)">编辑</el-button>
                            <el-popconfirm title="确定删除吗?" @confirm="deleteActionFromDialog(scope.row.id)">
                                <template #reference>
                                    <el-button link type="danger" size="small">删除</el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                 </el-table>
            </template>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="changeDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitChange">确定</el-button>
            </span>
        </template>
    </el-dialog>

    <!-- Create/Edit Action Item Dialog -->
    <el-dialog v-model="actionDialogVisible" :title="isEditAction ? '编辑行动项' : '添加行动项'" width="50%">
        <el-form :model="actionForm" label-width="120px">
            <el-form-item label="行动内容" required>
                <el-input v-model="actionForm.content" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="责任人" required>
                <el-input v-model="actionForm.owner" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="计划完成时间">
                <el-date-picker v-model="actionForm.plan_date" type="date" value-format="YYYY-MM-DD"></el-date-picker>
            </el-form-item>
            <el-form-item label="跟进人">
                <el-input v-model="actionForm.qa_contact"></el-input>
            </el-form-item>
            <el-form-item label="状态" v-if="isEditAction">
                <el-select v-model="actionForm.status">
                    <el-option label="待处理" value="Pending"></el-option>
                    <el-option label="已完成" value="Done"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="实际完成时间" v-if="actionForm.status === 'Done'">
                <el-date-picker v-model="actionForm.completed_at" type="date" value-format="YYYY-MM-DD"></el-date-picker>
            </el-form-item>
        </el-form>
        <template #footer>
             <span class="dialog-footer">
                <el-button @click="actionDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitAction">确定</el-button>
            </span>
        </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Download } from '@element-plus/icons-vue';
import { getChangeList, getActionList, createChange, updateChange, deleteChange, addActionItem, updateActionItem, deleteActionItem, exportChangeList } from '@/api/change_management';

const activeTab = ref('action_items');
const loading = ref(false);

const changeTableData = ref([]);
const actionTableData = ref([]);

const changeFilterStatus = ref('Open');
const actionFilterStatus = ref('Unfinished');
const searchKeyword = ref('');

const handleExport = async () => {
    try {
        const params = { status: changeFilterStatus.value, keyword: searchKeyword.value };
        const res = await exportChangeList(params);
        if (res.status === 200 && res.data) {
             const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
             const downloadElement = document.createElement('a');
             const href = window.URL.createObjectURL(blob);
             downloadElement.href = href;
             downloadElement.download = `变更流程导出_${new Date().toISOString().slice(0,10)}.xlsx`;
             document.body.appendChild(downloadElement);
             downloadElement.click();
             document.body.removeChild(downloadElement);
             window.URL.revokeObjectURL(href);
             ElMessage.success('导出成功');
        } else {
             ElMessage.error('导出失败');
        }
    } catch (e) {
        console.error(e);
        ElMessage.error('导出错误');
    }
};

const handleSearch = () => {
    if (activeTab.value === 'change_requests') fetchChangeData();
    else fetchActionData();
};

const handleTabClick = (tab) => {
    if (tab.props.name === 'change_requests') fetchChangeData();
    else fetchActionData();
};

const fetchChangeData = async () => {
    loading.value = true;
    try {
        const params = { status: changeFilterStatus.value, keyword: searchKeyword.value };
        const res = await getChangeList(params);
        if (res.data.success) changeTableData.value = res.data.data;
        else ElMessage.error(res.data.data || '获取变更数据失败');
    } catch (e) { ElMessage.error('网络错误'); }
    finally { loading.value = false; }
};

const fetchActionData = async () => {
    loading.value = true;
    try {
        const params = { status: actionFilterStatus.value };
        const res = await getActionList(params);
        if (res.data.success) actionTableData.value = res.data.data;
        else ElMessage.error(res.data.data || '获取行动项数据失败');
    } catch (e) { ElMessage.error('网络错误'); }
    finally { loading.value = false; }
};

const drawerVisible = ref(false);
const currentChangeInfo = ref(null);
const showChangeDrawer = (info) => { currentChangeInfo.value = info; drawerVisible.value = true; };

const changeDialogVisible = ref(false);
const isEditChange = ref(false);
const localActionItems = ref([]);
const changeForm = reactive({
    id: null, code: '', title: '', department: '', created_at: '', creator: '',
    description: '', level: '', impact_assessment: '', approval_date: '',
    cmo_agreed: false, cio_code: '', status: 'Open', close_date: ''
});

const showCreateDialog = () => {
    isEditChange.value = false;
    Object.assign(changeForm, {
        id: null, code: '', title: '', department: '', created_at: '', creator: '',
        description: '', level: '', impact_assessment: '', approval_date: '',
        cmo_agreed: false, cio_code: '', status: 'Open', close_date: ''
    });
    changeDialogVisible.value = true;
};

const editChange = (row) => {
    isEditChange.value = true;
    Object.assign(changeForm, row);
    localActionItems.value = JSON.parse(JSON.stringify(row.action_items || []));
    changeDialogVisible.value = true;
    drawerVisible.value = false;
};

const submitChange = async () => {
    if (changeForm.status === 'Closed') {
        if (!changeForm.close_date) changeForm.close_date = new Date().toISOString().split('T')[0];
        const unfinishedItems = localActionItems.value.filter(item => item.status !== 'Done');
        if (unfinishedItems.length > 0) {
            const itemDetails = unfinishedItems.map(i => `[${i.owner}] ${i.content}`).join('<br/>');
            try {
                await ElMessageBox.confirm(
                    `<p>以下工作项仍处于进行中：</p><div style="color: red; margin: 10px 0;">${itemDetails}</div><p>是否强制关闭该流程？</p>`,
                    '强制关闭确认',
                    { confirmButtonText: '强制关闭', cancelButtonText: '取消', type: 'warning', dangerouslyUseHTMLString: true }
                );
            } catch (e) { return; }
        }
    }
    try {
        let res;
        if (isEditChange.value) res = await updateChange(changeForm.id, changeForm);
        else res = await createChange(changeForm);
        if (res.data.success) {
            ElMessage.success('操作成功');
            changeDialogVisible.value = false;
            if (activeTab.value === 'change_requests') fetchChangeData();
            else fetchActionData();
        } else ElMessage.error(res.data.data || '操作失败');
    } catch (e) { ElMessage.error('网络错误'); }
};

const removeChange = async (id) => {
    try {
        const res = await deleteChange(id);
        if (res.data.success) { ElMessage.success('删除成功'); fetchChangeData(); }
        else ElMessage.error(res.data.data || '删除失败');
    } catch (e) { ElMessage.error('网络错误'); }
};

const actionDialogVisible = ref(false);
const isEditAction = ref(false);
const currentChangeId = ref(null);
const actionForm = reactive({
    id: null, content: '', owner: '', plan_date: '', qa_contact: '', status: 'Pending', completed_at: ''
});

const showAddActionDialog = (row) => {
    currentChangeId.value = row.id;
    isEditAction.value = false;
    Object.assign(actionForm, { id: null, content: '', owner: '', plan_date: '', qa_contact: '', status: 'Pending', completed_at: '' });
    actionDialogVisible.value = true;
};

const editActionItem = (row) => {
    currentChangeId.value = row.change_id;
    isEditAction.value = true;
    Object.assign(actionForm, row);
    actionDialogVisible.value = true;
};

const submitAction = async () => {
    try {
        let res;
        if (isEditAction.value) res = await updateActionItem(actionForm.id, actionForm);
        else res = await addActionItem({ ...actionForm, change_id: currentChangeId.value });
        if (res.data.success) {
            ElMessage.success('操作成功');
            actionDialogVisible.value = false;
            if (changeDialogVisible.value) {
                const newItem = res.data.data;
                if (isEditAction.value) {
                     const idx = localActionItems.value.findIndex(i => i.id === newItem.id);
                     if (idx !== -1) localActionItems.value[idx] = newItem;
                } else localActionItems.value.push(newItem);
            }
            if (activeTab.value === 'change_requests') fetchChangeData();
            else fetchActionData();
        } else ElMessage.error(res.data.data || '操作失败');
    } catch (e) { ElMessage.error('网络错误'); }
};

const deleteAction = async (itemId) => {
    try {
        const res = await deleteActionItem(itemId);
        if (res.data.success) {
            ElMessage.success('删除成功');
            if (activeTab.value === 'change_requests') fetchChangeData();
            else fetchActionData();
        } else ElMessage.error(res.data.data || '删除失败');
    } catch (e) { ElMessage.error('网络错误'); }
};

const deleteActionFromDialog = async (itemId) => {
    try {
        const res = await deleteActionItem(itemId);
        if (res.data.success) {
            ElMessage.success('删除成功');
            localActionItems.value = localActionItems.value.filter(i => i.id !== itemId);
            if (activeTab.value === 'change_requests') fetchChangeData();
        } else ElMessage.error(res.data.data || '删除失败');
    } catch (e) { ElMessage.error('网络错误'); }
};

onMounted(() => { fetchActionData(); });
</script>

<style scoped>
.header-actions { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 18px; font-weight: bold; }
.tab-filters { margin-bottom: 15px; display: flex; align-items: center; }
.label { margin-right: 10px; font-weight: bold; }
.detail-container { padding: 20px; background-color: #f9f9f9; }
.action-items-section { margin-top: 20px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.drawer-content { padding: 20px; }
.custom-search-input { width: 300px; margin-left: 20px; border-radius: 4px; }
.custom-search-input :deep(.el-input__wrapper) { box-shadow: 0 2px 6px rgba(0,0,0,0.08); border-radius: 20px; }
</style>

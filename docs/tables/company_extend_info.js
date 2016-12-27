/**
 * Created by zhaojm on 24/11/2016.
 */


// 公司常用信息表
// 其他地址来源的公司相关的信息，不唯一的信息
// 后面需要什么再添加
let company_extend_info =
{
    _id: "", // 自动生成ID
    company_id: "", // company_info._id

    state: "", // 状态
    introduce:// 公司描述
        [
            {
                update_time: "", // 存储时间
                from: "", // 来源
                content: "", //内容
            },
        ],
    address:// 公司地址
        [
            {
                update_time: "", // 存储时间
                from: "", // 来源
                content: "", //内容
            },
        ],
    people_num: // 公司规模
        [
            {
                update_time: "", // 存储时间
                from: "", // 来源
                content: "", //内容
            },
        ],
    website: // 公司网站
        [
            {
                update_time: "", // 存储时间
                from: "", // 来源
                content: "", //内容
            },
        ],
};
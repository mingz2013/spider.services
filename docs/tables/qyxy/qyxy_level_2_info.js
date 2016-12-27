/**
 * Created by zhaojm on 24/11/2016.
 */


// 公司公示信息


// 企业年报
let qynb_info =
{
    _id: "",
    company_id: "",

    update_time: "", // 发布日期
    year: "", // 年份

    company_base_info: // 企业基本信息
    {
        register_num: "",  // 注册号/统一社会信用代码
        company_name: "", // 企业名称
        phone: "", // 联系电话
        zipcode: "",//邮政编码
        address: "", // 企业通信地址
        email: "", // 电子邮箱
        is_gqzr: "", // 有限责任公司本年度是否发生股东股权转让
        status: "", // 企业经营状态
        is_have_website: "", // 是否有网站或网店
        is_have_tzxx: "", // 是否有投资信息或购买其他公司股权
        people_num: "", // 从业人数
    },

    website_info_list: // 网站或网店信息
        [
            {
                type: "", // 类型
                name: "", // 名称
                domain: "", // 网址
            },
        ],

    gdcz_info_list: // 股东及出资信息
        [
            {
                gd_name: "", // 投资人名称
                rjcz_je: "", // 认缴出资金额（万元）
                rjcz_type: "", // 认缴出资方式
                rjcz_time: "", // 认缴出资时间
                sjcz_je: "", // 实缴出资金额（万元）
                sjcz_type: "", // 实缴出资方式
                sjcz_time: "", // 实缴出资时间
            },
        ],

    dwtz_info_list: // 对外投资信息
        [
            {
                company_name: "", // 投资设立企业或购买股权企业名称
                register_num: "",  // 注册号/统一社会信用代码
            }
        ],

    qyzczk_info: // 企业资产状况信息
    {
        zczr: "", // 资产总额
        syzqyhj: "", // 所有者权益合计
        xsze: "", // 销售总额
        lrze: "", // 利润总额
        yyzsrzzyywsr: "", // 营业总收入中主营业务收入
        jlr: "", // 净利润
        nsze: "", // 纳税总额
        fzze: "", // 负债总额
    },

    dwtgdb_info_list: // 对外提供保证担保信息
        [
            {
                zqr: "", // 债权人
                zwr: "", // 债务人
                zzqzl: "", // 主债权种类
                zzqse: "", // 主债权数额
                lxzwdqx: "", // 履行债务的期限
                bzdqj: "", // 保证的期间
                bzdfs: "", // 保证的方式
                bzdbdfw: "", // 保证担保的范围
            }
        ],

    xgjl_info_list://修改记录
        [
            {
                xgsx: "", // 修改事项
                xgq: "", // 修改前
                xgh: "", // 修改后
                xgrq: "", // 修改日期
            }
        ],
    gdbg_info_list://股东变更
        [
            {
                "gd": "gd", // 股东
                "bgqbl": "bgqbl",  // 变更前股权比例
                "bghbl": "bghbl",  //变更后股权比例
                "bgrq": "bgrq", // 股权变更日期
            }
        ],
};


// 股东及出资信息
let gdcz_info =
{
    _id: "",
    company_id: "",

    gd_name: "", // 投资人名称
    rjcz_je: "", // 认缴出资金额（万元）
    rjmx:  // 认缴明细
        [
            {
                rjcz_type: "", // 认缴出资方式
                rjcz_je: "", // 认缴出资金额（万元）
                rjcz_time: "", // 认缴出资日期
            }
        ],

    sjcz_je: "", // 实缴出资金额（万元）
    sjmx: [ // 实缴明细
        {
            sjcz_je: "", // 实缴出资金额（万元）
            sjcz_type: "", // 实缴出资方式
            sjcz_time: "", // 实缴出资时间
        }
    ],
};


// 股权变更信息
let gdbg_info =
{
    _id: "",
    company_id: "",

    gd_name: "", // 股东
    bgqgqbl: "", // 变更前股权比例
    bghgqbl: "", // 变更后股权比例
    gqbgrq: "",// 股权变更日期
};


// 行政许可信息
let xzxk_info =
{
    _id: "",
    company_id: "",

    xkwjbh: "", // 许可文件编号
    xkwjmc: "", // 许可文件名称
    yxqzi: "", // 有效期自
    yzqzhi: "",// 有效期至
    xkjg: "",// 许可机关
    xknr: "", // 许可内容
    zt: "", // 状态
    xq: "", // 详情
};


// 知识产权出质登记信息
let zscqczdj_info =
{
    _id: "",
    company_id: "",

    zch: "", // 注册号
    mc: "", //名称
    zl: "", // 种类
    czrmc: "", // 出质人名称
    zqrmc: "",// 质权人名称
    zqdjqx: "", // 质权登记期限
    zt: "",// 	状态
    bhqk: "",// 	变化情况
};


// 行政处罚信息
let xzcf_info =
{
    _id: "",
    company_id: "",

    xzcfjdswh: "", //行政处罚决定书文号
    xzcfnr: "",// 	行政处罚内容
    zcxzcfjdjgmc: "",// 	作出行政处罚决定机关名称
    zcxzcfjdrq: "",// 	作出行政处罚决定日期
    wfxwlx: "",// 	违法行为类型
    bz: "",// 	备注
    xq: "",// 	详情
};



















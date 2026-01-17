-- 字段： stock_code,stock_name,latest_price,change_percent,shareholder_name,change_type,change_amount,change_total_ratio,
--     change_circulation_ratio,after_total_holdings,after_total_ratio,after_circulation_holdings,after_circulation_ratio,
--     change_start_date,change_end_date,announcement_date


-- 创建股东持股变动记录表
CREATE TABLE `shareholder_change_record` (
    -- 主键与基本信息
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID，自增主键',
    `stock_code` VARCHAR(20) COMMENT '股票代码',
    `stock_name` VARCHAR(50) COMMENT '股票名称',
    `latest_price` DECIMAL(10,2) COMMENT '最新价',
    `change_percent` DECIMAL(5,2) COMMENT '涨跌幅(%)',

    -- 股东信息
    `shareholder_name` VARCHAR(260) COMMENT '股东名称',
    `change_type` VARCHAR(10) COMMENT '持股变动类型-增减（如：减持、增持）',

    -- 变动信息
    `change_amount` DECIMAL(20,4) COMMENT '持股变动数量（万股）',
    `change_total_ratio` DECIMAL(10,6) COMMENT '变动数量占总股本比例(%)',
    `change_circulation_ratio` DECIMAL(10,6) COMMENT '变动数量占流通股比例(%)',

    -- 变动后持股情况
    `after_total_holdings` DECIMAL(20,4) COMMENT '变动后持股总数（万股）',
    `after_total_ratio` DECIMAL(10,6) COMMENT '变动后持股占总股本比例(%)',
    `after_circulation_holdings` DECIMAL(20,4) COMMENT '变动后持流通股数（万股）',
    `after_circulation_ratio` DECIMAL(10,6) COMMENT '变动后持股占流通股比例(%)',

    -- 时间信息
    `change_start_date` DATE COMMENT '变动开始日期',
    `change_end_date` DATE COMMENT '变动截止日期',
    `announcement_date` DATE COMMENT '公告日期',

    -- 系统字段
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    `is_deleted` TINYINT(1) DEFAULT 0 COMMENT '逻辑删除标记：0-正常，1-已删除',

    -- 索引
    PRIMARY KEY (`id`),
    INDEX `idx_stock_code` (`stock_code`),
    INDEX `idx_shareholder_name` (`shareholder_name`(100)),
    INDEX `idx_change_date` (`change_start_date`, `change_end_date`),
    INDEX `idx_announcement_date` (`announcement_date`),
    INDEX `idx_change_type` (`change_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股东持股变动记录表';


-- demo:
-- 代码      名称      最新价   涨跌幅       股东名称     持股变动信息-增减  持股变动信息-变动数量  持股变动信息-占总股本比例  持股变动信息-占流通股比例  变动后持股情况-持股总数  变动后持股情况-占总股本比例  变动后持股情况-持流通股数  变动后持股情况-占流通股比例       变动开始日       变动截止日         公告日
-- 920367   新赣江     22.28    6.86        张明          减持           54.4083                 0.767815           1.30                    443.6863            6.26                        443.6863               10.62                    2025-11-21    2026-01-09       2026-01-09
-- 920367   新赣江     22.28    6.86        张咪          减持           2.5744                  0.036330           0.06                    246.4754            3.48                        246.4754               5.90                     2025-11-21    2026-01-09       2026-01-09
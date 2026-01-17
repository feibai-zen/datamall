
-- 字段： stock_code,stock_name,release_time,restricted_share_type,release_quantity,actual_release_quantity,
--     actual_release_market_value,proportion_of_released_market_value,closing_price_before_release_day,
--     price_change_rate_20_days_before_release,price_change_rate_20_days_after_release


-- 创建 限售股解禁详情 表
CREATE TABLE `restricted_shares_release_detail` (
    -- 主键与基本信息
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID, 自增主键',
    `stock_code` VARCHAR(20) COMMENT '股票代码',
    `stock_name` VARCHAR(50) COMMENT '股票简称',

    -- 变动信息
    `release_time` DATE COMMENT '解禁时间',
    `restricted_share_type` VARCHAR(50) COMMENT '限售股类型',
    `release_quantity` DECIMAL(20,4) COMMENT '解禁数量',
    `actual_release_quantity` DECIMAL(20,4) COMMENT '实际解禁数量',
    `actual_release_market_value` DECIMAL(20,4) COMMENT '实际解禁市值',
    `proportion_of_released_market_value` DECIMAL(10,6) COMMENT '占解禁前流通市值比例',

    -- 价格信息
    `closing_price_before_release_day` DECIMAL(10,2) COMMENT '解禁前一交易日收盘价',
    `price_change_rate_20_days_before_release` DECIMAL(10,6) COMMENT '解禁前20日涨跌幅',
    `price_change_rate_20_days_after_release` DECIMAL(10,6) COMMENT '解禁后20日涨跌幅',

    -- 系统字段
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    `is_deleted` TINYINT(1) DEFAULT 0 COMMENT '逻辑删除标记：0-正常，1-已删除',

    -- 索引
    PRIMARY KEY (`id`),
    INDEX `idx_stock_code` (`stock_code`),
    INDEX `idx_release_time` (`release_time`),
    INDEX `idx_c_share_type` (`restricted_share_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票解禁信息表';

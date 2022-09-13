DROP TABLE IF EXISTS collect;
CREATE TABLE collect
(
    id         INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID',
    pid        INT          NOT NULL COMMENT 'pid',
    title      VARCHAR(50)  NOT NULL COMMENT '标题',
    urls       VARCHAR(600) NOT NULL COMMENT '图片地址字典,json序列化',
    tags       VARCHAR(300) NOT NULL COMMENT '标签,含翻译',
    uid        INT          NOT NULL COMMENT 'uiD',
    author     VARCHAR(20)  NOT NULL COMMENT '作者',
    width      INT          NOT NULL COMMENT '宽度',
    height     INT          NOT NULL COMMENT '高度',
    page_count INT          NOT NULL COMMENT '作品所在页数',
    r18        INT          NOT NULL COMMENT 'r18-1,非r18-0'
);

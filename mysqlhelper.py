# -*- coding: utf-8 -*-
# @Time    : 2021/6/6 20:19
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : mysqlhelper.py

import pymysql
import sys
import copy


class MysqlHelper:

    def __init__(self, mysql_config):
        self.mysql_config = mysql_config

    def mysql_create(self, connection, sql):
        """创建MySQL数据库或表"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        finally:
            connection.close()

    def mysql_create_database(self, sql):
        """创建MySQL数据库"""
        try:
            import pymysql
        except ImportError:
            raise Exception('系统中可能没有安装pymysql库，请先运行 pip install pymysql ，再运行程序')
        mysql_config = copy.deepcopy(self.mysql_config)
        mysql_config.pop("database")
        try:
            connection = pymysql.connect(**mysql_config)
            self.mysql_create(connection, sql)
        except pymysql.OperationalError:
            raise Exception(u'系统中可能没有安装或正确配置MySQL数据库，请先根据系统环境安装或配置MySQL，再运行程序')
            # sys.exit()

    def mysql_create_table(self, sql):
        """创建MySQL表"""

        connection = pymysql.connect(**self.mysql_config)
        self.mysql_create(connection, sql)

    def mysql_insert(self, table, data_list):
        """向MySQL表插入或更新数据"""
        import pymysql

        if len(data_list) > 0:
            keys = ', '.join(data_list[0].keys())
            values = ', '.join(['%s'] * len(data_list[0]))
            connection = pymysql.connect(**self.mysql_config)
            cursor = connection.cursor()
            sql = """INSERT INTO `{table}`({keys}) VALUES ({values}) ON
                         DUPLICATE KEY UPDATE""".format(table=table,
                                                        keys=keys,
                                                        values=values)
            update = ','.join([
                ' {key} = values({key})'.format(key=key)
                for key in data_list[0]
            ])
            sql += update

            try:
                cursor.executemany(
                    sql, [tuple(data.values()) for data in data_list])
                connection.commit()
            except Exception as e:
                connection.rollback()
                print(sql)
                print("mysql_helper",e)
                print("mysql_helper",type(e))
                # logger.exception(e)
            finally:
                connection.close()

    def data_to_mysql(self, data_list, table_config):
        """将爬取的微博信息写入MySQL数据库"""
        # mysql_config = {
        #     'host': 'localhost',
        #     'port': 3306,
        #     'user': 'root',
        #     'password': '',
        #     'charset': 'utf8mb4'
        # }
        # 创建数据库
        create_database = """CREATE DATABASE IF NOT EXISTS {database} DEFAULT
                                    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""".format(
            database=self.mysql_config.get("database"))

        # print(create_database)
        self.mysql_create_database(create_database)

        # 创建表
        create_table = table_config.get("create_table")
        self.mysql_create_table(create_table)
        # weibo_list = []
        # retweet_list = []
        # if len(self.write_mode) > 1:
        #     info_list = copy.deepcopy(self.weibo[wrote_count:])
        # else:
        #     info_list = self.weibo[wrote_count:]
        # for w in info_list:
        #     if 'retweet' in w:
        #         w['retweet']['retweet_id'] = ''
        #         retweet_list.append(w['retweet'])
        #         w['retweet_id'] = w['retweet']['id']
        #         del w['retweet']
        #     else:
        #         w['retweet_id'] = ''
        #     weibo_list.append(w)
        # 在'weibo'表中插入或更新微博数据
        self.mysql_insert(table_config.get("table"), data_list)
        # self.mysql_insert(mysql_config, 'weibo', weibo_list)
        # logger.info(u'%d条数据写入MySQL数据库完毕', self.got_count)


if __name__ == '__main__':
    mysql_config = {
        'host': '47.93.119.185',
        'port': 3306,
        'user': 'social',
        'password': 'moonshine**1',
        'charset': 'utf8mb4',
        "database": "opinion"

    }

    mysql_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'charset': 'utf8mb4',
        "database": "opinion"
    }
    table_config = {
        "table": "yqt",
        "create_table": """
                    CREATE TABLE IF NOT EXISTS yqt (
                    id int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
                    start_word varchar(100),
                    publish_date DATETIME,
                    title text,
                    content text ,
                    repost_content text ,
                    url varchar(1024),
                    poster varchar(1000),
                    attitude  varchar(100),
                    images text,
                    reposts_count INT,
                    comments_count INT,
                    sort varchar(100),  
                    industry  varchar(100),
                    related_words varchar(100),
                    site_name varchar(100),
                    area  varchar(100),
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    update_time DATETIME,
                    PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

    }

    table_config = {
        "table": "topic",
        "create_table": """CREATE TABLE `topic` (
        
          `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
          site varchar(32) COMMENT '站点',
          start_word varchar(100) COMMENT '搜索词',
          `url` text COMMENT '文章链接',
          `title` text COMMENT '标题',
          `content` text COMMENT '正文',
          `publish_date` datetime DEFAULT NULL COMMENT '发表时间',
          `author` varchar(32) DEFAULT NULL COMMENT '作者',
          `author_home_url` text COMMENT '作者主页',
          `auth` varchar(32) DEFAULT NULL COMMENT '认证',
          `author_head_img_url` text COMMENT '头像链接',
          `type` varchar(16) DEFAULT NULL COMMENT '文章类型',
          `device` varchar(32) DEFAULT NULL COMMENT '设备',
          `viewed_num` int(11) DEFAULT NULL COMMENT '浏览数',
          `liked_num` int(11) DEFAULT NULL COMMENT '点赞数',
          `forwarded_num` int(11) DEFAULT NULL COMMENT '转发数',
          `commented_num` int(11) DEFAULT NULL COMMENT '评论数',
          `collected_num` int(11) DEFAULT NULL COMMENT '收藏数',
          `focused_num` int(11) DEFAULT NULL COMMENT '关注数',
          `disagreed_num` int(11) DEFAULT NULL COMMENT '踩数',
          `star_num` float DEFAULT NULL COMMENT '星星数',
          `description` text COMMENT '描述',
          `image_url` text COMMENT '图片链接',
          `cover_img_url` text COMMENT '封面图片链接',
          `belong_board` varchar(16) DEFAULT NULL COMMENT '所属板块',
          `root_id` varchar(32) DEFAULT NULL COMMENT '原始id',
          `status` int(11) DEFAULT NULL COMMENT '状态',
          `author_id` int(11) DEFAULT NULL,
          `author_des` text COMMENT '作者简介',
          `music_title` text COMMENT '音乐标题',
          `music_url` text COMMENT '音乐链接',
          `video_url` text COMMENT '视频链接',
          dy_sec_uid varchar(200) COMMENT '抖音sec_uid',
          `author_uid` varchar(64) DEFAULT NULL COMMENT '作者id',
            `create_time` datetime DEFAULT NULL COMMENT '入库时间',
          `update_time` datetime DEFAULT NULL COMMENT '更新时间',
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=143236 DEFAULT CHARSET=utf8mb4;"""

    }
    mysql_helper = MysqlHelper(mysql_config)

    mysql_helper.data_to_mysql(data_list=[], table_config=table_config)

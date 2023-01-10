-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.

-- member Table Create SQL
CREATE TABLE member
(
    `memID`        VARCHAR(30)    NOT NULL    COMMENT '회원 아이디', 
    `memPw`        VARCHAR(30)    NOT NULL    COMMENT '회원 비밀번호', 
    `memName`      VARCHAR(30)    NOT NULL    COMMENT '회원 이름', 
    `memCompany`   VARCHAR(30)    NOT NULL    COMMENT '회원 소속회사', 
    `memType`      CHAR(1)        NOT NULL    DEFAULT 'W' COMMENT '회원 유형. 일반유저:''U'', 관리자:''A'', 대기유저 : ''W''', 
    `memJoindate`  DATETIME       NOT NULL    DEFAULT NOW() COMMENT '회원 가입일자', 
     PRIMARY KEY (memID)
);

ALTER TABLE member COMMENT '회원 관리';


-- board Table Create SQL
CREATE TABLE board
(
    `boardSeq`      INT UNSIGNED    NOT NULL    AUTO_INCREMENT COMMENT '글 번호', 
    `boardTitle`    VARCHAR(400)    NOT NULL    COMMENT '글 제목', 
    `boardContent`  TEXT            NOT NULL    COMMENT '글 내용', 
    `boardDate`     DATETIME        NOT NULL    DEFAULT NOW() COMMENT '글 작성일자', 
    `memID`         VARCHAR(30)     NOT NULL    COMMENT '글 작성자', 
    `boardCnt`      INT             NOT NULL    DEFAULT 0 COMMENT '글 조회수', 
     PRIMARY KEY (boardSeq)
);

ALTER TABLE board COMMENT '회원 게시판';

ALTER TABLE board
    ADD CONSTRAINT FK_board_memID_member_memID FOREIGN KEY (memID)
        REFERENCES member (memID) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- cosmetic Table Create SQL
CREATE TABLE cosmetic
(
    `productID`              VARCHAR(30)      NOT NULL    COMMENT '제품 아이디', 
    `productNM`              VARCHAR(200)     NOT NULL    COMMENT '제품 명', 
    `productImg`             VARCHAR(400)     NOT NULL    COMMENT '제품 이미지', 
    `productCharacter`       VARCHAR(200)     NOT NULL    COMMENT '제품 특징', 
    `productStar`            DECIMAL(3, 1)    NOT NULL    DEFAULT 0 COMMENT '제품 평점', 
    `productMaker`           VARCHAR(50)      NOT NULL    COMMENT '제품 제조사', 
    `productBrand`           VARCHAR(50)      NOT NULL    COMMENT '제품 브랜드', 
    `productDate`            VARCHAR(10)      NOT NULL    COMMENT '제품 등록일자', 
    `productReviewCnt`       INT              NOT NULL    DEFAULT 0 COMMENT '제품 리뷰개수', 
    `productIngredient`      TEXT             NOT NULL    COMMENT '제품 성분', 
    `productStarRatio`       VARCHAR(50)      NOT NULL    COMMENT '제품 평점 비율', 
    `productAgeLikes`        VARCHAR(45)      NOT NULL    COMMENT '제품 연령별 선호도', 
    `productSexLikes`        VARCHAR(45)      NOT NULL    COMMENT '제품 성별 선호도', 
    `productEwgScore`        VARCHAR(300)     NOT NULL    COMMENT '제품 EWG 점수', 
    `productDryScore`        VARCHAR(300)     NOT NULL    COMMENT '제품 건성 지수', 
    `productOilScore`        VARCHAR(300)     NOT NULL    COMMENT '제품 지성 지수', 
    `productSensitiveScore`  VARCHAR(300)     NOT NULL    COMMENT '제품 민감성 지수', 
    `productAllegyScore`     VARCHAR(300)     NOT NULL    COMMENT '제품 알러지 지수', 
    `productType`            CHAR(1)          NOT NULL    COMMENT '제품 타입', 
    `productRank`            INT              NOT NULL    DEFAULT 0 COMMENT '제품 트랜드 랭킹', 
    `productKeyword`         TEXT             NULL        COMMENT '제품 키워드', 
     PRIMARY KEY (productID)
);

ALTER TABLE cosmetic COMMENT '화장품 제품 데이터';


-- comment Table Create SQL
CREATE TABLE comment
(
    `cmtSeq`     INT UNSIGNED    NOT NULL    AUTO_INCREMENT COMMENT '댓글 순번', 
    `boardSeq`   INT UNSIGNED    NOT NULL    COMMENT '원글 순번', 
    `cmtConten`  TEXT            NOT NULL    COMMENT '댓글 내용', 
    `cmtDate`    DATETIME        NOT NULL    DEFAULT NOW() COMMENT '댓글 작성일자', 
    `memID`      VARCHAR(30)     NOT NULL    COMMENT '댓글 작성자', 
     PRIMARY KEY (cmtSeq)
);

ALTER TABLE comment COMMENT '댓글';

ALTER TABLE comment
    ADD CONSTRAINT FK_comment_memID_member_memID FOREIGN KEY (memID)
        REFERENCES member (memID) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE comment
    ADD CONSTRAINT FK_comment_boardSeq_board_boar FOREIGN KEY (boardSeq)
        REFERENCES board (boardSeq) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- ingredient Table Create SQL
CREATE TABLE ingredient
(
    `ingreCode`            INT              NOT NULL    COMMENT '성분 코드', 
    `ingreName`            VARCHAR(2000)    NOT NULL    COMMENT '성분 이름', 
    `ingreEngName`         VARCHAR(2000)    NOT NULL    COMMENT '성분 영어명', 
    `ingreCas`             VARCHAR(200)     NOT NULL    COMMENT '성분 CAS', 
    `ingreOldName`         VARCHAR(2000)    NOT NULL    COMMENT '성분 구명칭', 
    `ingreEwg`             VARCHAR(10)      NOT NULL    COMMENT '성분 Ewg 점수', 
    `ingreEwgData`         VARCHAR(100)      NOT NULL    COMMENT '성분 Ewg 등급', 
    `IngreObj`             VARCHAR(500)     NOT NULL    COMMENT '성분 배합목적', 
    `ingreDryScore`        INT              NOT NULL    DEFAULT 0 COMMENT '성분 건성 지수', 
    `ingreOilScore`        INT              NOT NULL    DEFAULT 0 COMMENT '성분 지성 지수', 
    `ingreSensitiveScore`  INT              NOT NULL    DEFAULT 0 COMMENT '성분 민감성 지수', 
    `ingreAllegyScore`     INT              NOT NULL    DEFAULT 0 COMMENT '성분 알러지 지수', 
    `ingreSkinRanking`     INT              NOT NULL    DEFAULT 0 COMMENT '성분 스킨 랭킹', 
    `ingreCreamRanking`    INT              NOT NULL    DEFAULT 0 COMMENT '성분 크림 랭킹', 
    `ingreLotionRanking`    INT              NOT NULL    DEFAULT 0 COMMENT '성분 로션 랭킹', 
    `ingreKeyword`         TEXT             NULL        COMMENT '성분 키워드', 
    `ingreProduct`         VARCHAR(300)     NULL        COMMENT '성분 관련 제품', 
    `ingreTogether`        VARCHAR(300)     NULL        COMMENT '성분 관련 성분', 
     PRIMARY KEY (ingreCode)
);

ALTER TABLE ingredient COMMENT '화장품 크롤링 데이터';

DROP TABLE if exists ingredient;
DROP TABLE if exists cosmetic;

TRUNCATE table cosmetic ;
TRUNCATE table ingredient; 
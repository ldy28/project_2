package com.example.entity;

import lombok.Data;

@Data
public class Cosmetic {
	
    private String productID;

    // 제품 명 
    private String productNM;

    // 제품 이미지 
    private String productImg;

    // 제품 평점 
    private double productStar;
    
    // 제품 특징
    private String productCharacter;

    // 제품 제조사 
    private String productMaker;

    // 제품 브랜드 
    private String productBrand;

    // 제품 등록일자 
    private String productDate;

    // 제품 리뷰수 
    private Integer productReviewCnt;

    // 제품 성분 
    private String productIngredient;

    // 제품 평점 비율 
    private String productStarRatio;

    // 제품 연령별 선호도 
    private String productAgeLikes;

    // 제품 성별 선호도 
    private String productSexLikes;

    private String productEwgScore;
    
    private String productDryScore;
    
    private String productOilScore;
    
    private String productSensitiveScore;
    
    private String productAllegyScore;
    

    // 제품 타입 
    private String productType;

    // 제품 트렌드여부 
    private Integer productRank;
    
    private String productKeyword;
    
 // 관리자 아이디 
    private String adminID;
}

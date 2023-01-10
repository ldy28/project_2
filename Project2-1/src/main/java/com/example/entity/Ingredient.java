package com.example.entity;

import lombok.Data;
import lombok.ToString;

@Data
@ToString
public class Ingredient {
	 // 성분 코드 
    private Integer ingreCode;

    // 성분 명 
    private String ingreName;

    // 성분 영어명 
    private String ingreEngName;

    // 성분 화학식 
    private String ingreCas;

    // 성분 옛이름 
    private String ingreOldName;

    // 성분 등급 
    private String ingreEwg;

    // 성분 등급 데이터 
    private String ingreEwgData;

    private int ingreAllegyScore;

    // 성분 배합 목적 
    private String ingreObj;

    // 성분 트렌드 여부 
    private int ingreRank;
    
    private int ingreOilScore;
    private int ingreDryScore;
    private int ingreSensitiveScore;
    
    private int ingreSkinRanking;
    private int ingreCreamRanking;
    private int ingreLotionRanking;
    private String ingreProduct;
    private String ingreKeyword;
}


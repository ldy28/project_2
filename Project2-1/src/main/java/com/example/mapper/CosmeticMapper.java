package com.example.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import com.example.entity.Board;
import com.example.entity.Criteria;
import com.example.entity.Ingredient;
import com.example.entity.Cosmetic;

@Mapper
public interface CosmeticMapper {
	public List<Board> list(Criteria cri);

	public int countBoard(Criteria cri);

	public List<Ingredient> ingreList(Criteria cri);

	public int countIngre(Criteria cri);

	public List<Cosmetic> cosmeticList(Criteria cri);

	public int countCosmetic(Criteria cri);

	@Select("select * from cosmetic where productID = #{productID}")
	public Cosmetic cosDetail(String productID);

	@Select("select * from ingredient where ingreCode = #{ingreCode}")
	public Ingredient ingreDetail(int ingreCode);

	public List<Cosmetic> ingreProduct(List<String> li1);

	

	

	
}

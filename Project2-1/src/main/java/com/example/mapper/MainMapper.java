package com.example.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.example.entity.Cosmetic;
import com.example.entity.Ingredient;

@Mapper
public interface MainMapper {

	public List<Ingredient> rankIngre(String type);

	public List<Cosmetic> rankCos(String type);
	
}

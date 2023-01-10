package com.example.service;

import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Cosmetic;
import com.example.entity.Criteria;
import com.example.entity.Ingredient;
import com.example.mapper.CosmeticMapper;

@Service
public class IngreService {

	@Autowired
	CosmeticMapper cosmeticMapper;
	
	public List<Ingredient> ingreList(Criteria cri){
		List<Ingredient> list = cosmeticMapper.ingreList(cri);
		return list;
	}
	
	public int countIngre(Criteria cri) {
		// TODO Auto-generated method stub
		return cosmeticMapper.countIngre(cri);
	}

	public Ingredient ingreDetail(int ingreCode) {
		
		
		return cosmeticMapper.ingreDetail(ingreCode);
	}

	public List<Cosmetic> ingreProduct(List<String> li1) {
		
		return cosmeticMapper.ingreProduct(li1);
	}
	
}

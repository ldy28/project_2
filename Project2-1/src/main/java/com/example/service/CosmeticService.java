package com.example.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Criteria;
import com.example.entity.Cosmetic;
import com.example.mapper.CosmeticMapper;

@Service
public class CosmeticService {
	@Autowired
	CosmeticMapper cosmeticMapper;

	public List<Cosmetic> cosmeticList(Criteria cri) {

		List<Cosmetic> list = cosmeticMapper.cosmeticList(cri);

		// "|" -> "," 바꿔주기
		for (Cosmetic cos : list) {
			cos.setProductCharacter(cos.getProductCharacter().replace("|", ","));
		}

		return list;
	}

	public int countCosmetic(Criteria cri) {
		// TODO Auto-generated method stub
		return cosmeticMapper.countCosmetic(cri);
	}

	public Cosmetic cosDetail(String productID) {

		return cosmeticMapper.cosDetail(productID);
	}
}

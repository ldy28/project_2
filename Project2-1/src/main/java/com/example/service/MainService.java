package com.example.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Cosmetic;
import com.example.entity.Ingredient;
import com.example.mapper.MainMapper;

@Service
public class MainService {
	
	@Autowired
	MainMapper mainMapper;

	public List<Ingredient> rankIngre(String type) {
		
		return mainMapper.rankIngre(type);
	}

	public List<Cosmetic> rankCos(String type) {
		
		return mainMapper.rankCos(type);
	}

}

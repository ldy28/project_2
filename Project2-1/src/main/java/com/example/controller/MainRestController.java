package com.example.controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.entity.Cosmetic;
import com.example.entity.Ingredient;
import com.example.service.MainService;

@RestController
public class MainRestController {
	@Autowired
	MainService mainService;
	
	@RequestMapping("/mainIngre")
	
	public List<Ingredient> mainIngre(@RequestParam("type") String type){
		System.out.println(type);
		return mainService.rankIngre(type);
	}
	
	@RequestMapping("/mainCos")
	
	public List<Cosmetic> mainCos(@RequestParam("type") String type){
		return mainService.rankCos(type);
	}
	
	
}

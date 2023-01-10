package com.example.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.entity.Cosmetic;
import com.example.entity.Criteria;
import com.example.entity.PageMaker;
import com.example.service.CosmeticService;

@RestController
public class CosRestController {
	@Autowired
	CosmeticService cosmeticService;
	
	@RequestMapping("/cosmeticList")
	public Map<String,Object> cosmetic(Criteria cri) {
		List<Cosmetic> list = cosmeticService.cosmeticList(cri);
		
		
		System.out.println(cri);
		System.out.println(list);
		
		PageMaker pageMaker = new PageMaker();
		pageMaker.setCri(cri);
		int cnt = cosmeticService.countCosmetic(cri);
		pageMaker.setTotalCount(cnt);
		System.out.println(pageMaker.getStartPage());
		System.out.println(pageMaker.getEndPage());
		Map<String,Object> m = new HashMap<>();
		m.put("list", list);
		m.put("pageMaker", pageMaker);
		
		return m;
	
	
	}
	
}

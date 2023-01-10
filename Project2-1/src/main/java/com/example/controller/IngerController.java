package com.example.controller;

import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.entity.Cosmetic;
import com.example.entity.Criteria;
import com.example.entity.Ingredient;
import com.example.entity.PageMaker;
import com.example.service.IngreService;

@Controller
public class IngerController {
	
	@Autowired
	IngreService ingreService;
	
	@RequestMapping("ingreList.do")
	public String ingreList(Model model, Criteria cri) {
		List<Ingredient> list = ingreService.ingreList(cri);
		
		for (Ingredient ingre : list) {
			ingre.setIngreObj(ingre.getIngreObj().replace("|", ","));
		}
		model.addAttribute("ingreList",list);
		System.out.println(cri);
		System.out.println(list);
		
		PageMaker pageMaker = new PageMaker();
		pageMaker.setCri(cri);
		pageMaker.setTotalCount(ingreService.countIngre(cri));
		System.out.println(pageMaker.getStartPage());
		System.out.println(pageMaker.getEndPage());
		model.addAttribute("pageMaker",pageMaker);
		return "th/ingre";
	}
	
	@RequestMapping("/ingreDetail")
	public String ingreDetail(@RequestParam("ingreCode") int ingreCode ,Model model) {
		Ingredient ingre = ingreService.ingreDetail(ingreCode);
		List<String> li1 = Arrays.asList(ingre.getIngreProduct().split("[|]"));
		
		List<Cosmetic> cosList = ingreService.ingreProduct(li1);
		System.out.println(ingre);
		System.out.println(cosList);
		model.addAttribute("ingre",ingre);
		model.addAttribute("cosList",cosList);
		
		return "th/ingreDetail";
	}
	
}

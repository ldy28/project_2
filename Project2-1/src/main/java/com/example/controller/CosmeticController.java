package com.example.controller;

import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.entity.Cosmetic;
import com.example.entity.Criteria;
import com.example.entity.PageMaker;
import com.example.entity.productIngre;
import com.example.service.CosmeticService;
import com.google.gson.Gson;

@Controller
public class CosmeticController {
	@Autowired
	CosmeticService cosmeticService;

	@RequestMapping("/cosmeticList.do")
	public String cosmeticList(Model model, Criteria cri) {
		List<Cosmetic> list = cosmeticService.cosmeticList(cri);

		model.addAttribute("cosmeticList", list);
		System.out.println(cri);
		System.out.println(list);

		PageMaker pageMaker = new PageMaker();
		pageMaker.setCri(cri);
		int cnt = cosmeticService.countCosmetic(cri);
		pageMaker.setTotalCount(cnt);
		System.out.println(pageMaker.getStartPage());
		System.out.println(pageMaker.getEndPage());
		model.addAttribute("pageMaker", pageMaker);
		model.addAttribute("cnt", cnt);
		return "th/cosmetic";

	}

	@RequestMapping("/cosDetail")
	public String cosDetail(@RequestParam("productID") String productID, Model model) {

		Cosmetic cos = cosmeticService.cosDetail(productID);
		List<String> dryList = Arrays.asList(cos.getProductDryScore().split("[|]"));
		List<String> oilList = Arrays.asList(cos.getProductOilScore().split("[|]"));
		List<String> senList = Arrays.asList(cos.getProductSensitiveScore().split("[|]"));
		List<String> allList = Arrays.asList(cos.getProductAllegyScore().split("[|]"));

		List<Integer> ingre = new ArrayList<>();
		ingre.add(Collections.frequency(oilList, "1"));
		ingre.add(Collections.frequency(oilList, "2"));
		ingre.add(Collections.frequency(dryList, "1"));
		ingre.add(Collections.frequency(dryList, "2"));
		ingre.add(Collections.frequency(senList, "1"));
		ingre.add(Collections.frequency(senList, "2"));
		ingre.add(Collections.frequency(allList, "1"));

		List<String> ewgList = Arrays.asList(cos.getProductEwgScore().replaceAll("-[0-9]", "").split("[|]"));
		String ewg = "";

		ewg = ewg + Integer.toString(Collections.frequency(ewgList, "1") + Collections.frequency(ewgList, "2")) + ",";
		ewg = ewg + Integer.toString(Collections.frequency(ewgList, "3") + Collections.frequency(ewgList, "4")
				+ Collections.frequency(ewgList, "5") + Collections.frequency(ewgList, "6")) + ",";
		ewg = ewg + Integer.toString(Collections.frequency(ewgList, "7") + Collections.frequency(ewgList, "8")
				+ Collections.frequency(ewgList, "9") + Collections.frequency(ewgList, "10")) + ",";
		ewg = ewg + Integer.toString(Collections.frequency(ewgList, "0"));

		List<String> productIngre = Arrays.asList(cos.getProductIngredient().split("[|]"));
		List<String> productIngreEwg = Arrays.asList(cos.getProductEwgScore().split("[|]"));

		List<com.example.entity.productIngre> proList = new ArrayList<>();
		for (int i = 0; i < productIngre.size(); i++) {
			com.example.entity.productIngre pro = new productIngre();
			pro.setProductEwgScore(productIngreEwg.get(i));
			pro.setProductIngredient(productIngre.get(i));
			proList.add(pro);
		}

		System.out.println(ewg);
		Gson gson = new Gson();
		String json = gson.toJson(ingre);
		model.addAttribute("ewg", ewg);
		model.addAttribute("json", json);
		model.addAttribute("cos", cos);
		model.addAttribute("proList", proList);
		return "th/cosDetail";

	}
}

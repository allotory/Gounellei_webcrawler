package com.crawler.zhihu.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RealURL {
	public static String getRealURL(String url) {
		Pattern pattern = Pattern.compile("question/(.*?)/");
		Matcher matcher = pattern.matcher(url);
		String zhihuURL = "";
		if (matcher.find()) {
			zhihuURL = "http://www.zhihu.com/question/" + matcher.group(1);
		} else {
			zhihuURL = url;
		}
		return zhihuURL;
	}
}

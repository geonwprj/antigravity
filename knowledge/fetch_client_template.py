import httpx
import re
import json
from urllib.parse import quote, urlparse
import asyncio
import random
from typing import Dict, Tuple, Union, Optional
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
from datetime import datetime
from enum import Enum

class REQUEST_METHOD(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class FetchClient:
    """
    Standard robust httpx client with retries and HTML processing.
    """
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def url_builder(self, base_url: str, path: str, **kwargs) -> str:
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        url_part = urlparse(url)
        base_url = f"{url_part.scheme}://{url_part.netloc}"
        path = url_part.path
        if path.endswith('/'):
            if len(path.split(".")) > 1:
                path = path.rstrip('/')
        for k, v in kwargs.items():
            matches = re.search(f"{{{{{k}}}}}", path)
            if not matches:
                continue
            if isinstance(v, dict):
                val = json.dumps(v)
            elif isinstance(v, list):
                val = json.dumps(v)
            elif isinstance(v, str):
                val = v
            elif isinstance(v, bool):
                val = str(v).lower()
            elif isinstance(v, int):
                val = str(v)
            elif isinstance(v, float):
                val = str(v)
            elif isinstance(v, datetime):
                val = v.isoformat()
            path = path.replace(matches.group(0), val)  
        return f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    async def fetch(self, url: str, method: str = "GET", headers: dict = None, params: dict = None, data: dict = None, json_data: dict = None, files: dict = None, timeout: int = 30, retries: int = 3, **kwargs):
        if headers:
            new_headers = self.headers.copy()
            new_headers.update(headers)
            headers = new_headers
        else:
            headers = self.headers.copy()

        if files and 'content-type' in [h.lower() for h in headers.keys()]:
            content_type_key = next(h for h in headers.keys() if h.lower() == 'content-type')
            del headers[content_type_key]
        
        last_exception = None
        for attempt in range(retries):
            try:
                method = method.upper()
                response = await self.client.request(
                    method=method, 
                    url=url, 
                    headers=headers, 
                    params=params, 
                    data=data, 
                    json=json_data, 
                    files=files, 
                    timeout=timeout, 
                    **kwargs
                )
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                should_retry = False
                if isinstance(e, httpx.HTTPStatusError) and e.response.status_code >= 500:
                    should_retry = True
                elif isinstance(e, httpx.RequestError):
                    should_retry = True
                
                if should_retry and attempt < retries - 1:
                    last_exception = e
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(sleep_time)
                else:
                    raise e
        
        if last_exception:
            raise last_exception

    def shorten_text(self, text: str, limit: int) -> str:
        if len(text) <= 2 * limit:
            return text
        return f"{text[:limit]} ... [trimmed {len(text) - 2*limit} chars] ... {text[-limit:]}"

    def process_html_for_llm(self, soup: Union[BeautifulSoup, str], keep_first_last: int = 2, p_first_last_chars: int = 100) -> str:
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, "html.parser")
        
        useless_tags = ['script', 'style', 'noscript', 'svg', 'meta', 'link', 'iframe', 'head']
        for element in soup(useless_tags):
            element.decompose()

        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        def process_siblings(parent: Union[BeautifulSoup, Tag]) -> None:
            children = list(parent.children)
            i = 0
            while i < len(children):
                child = children[i]
                if child.parent is None: 
                    i += 1
                    continue
                if isinstance(child, Tag):
                    if child.name in ['li', 'p', 'br']:
                        seq = [child]
                        sibling = child.next_sibling
                        while sibling:
                            if isinstance(sibling, Tag) and sibling.name == child.name:
                                seq.append(sibling)
                                sibling = sibling.next_sibling
                            elif isinstance(sibling, NavigableString) and not sibling.strip():
                                sibling = sibling.next_sibling
                            else:
                                break
                        if len(seq) > 2 * keep_first_last:
                            to_remove = seq[keep_first_last:-keep_first_last]
                            for item in to_remove:
                                item.decompose()
                            placeholder = soup.new_tag("div")
                            placeholder.string = f"... [{len(to_remove)} {child.name} items removed] ..."
                            seq[keep_first_last-1].insert_after(placeholder)
                    
                    if child.name == 'p' and child.string:
                        text = child.string
                        if len(text) > 2 * p_first_last_chars:
                            new_text = self.shorten_text(text, p_first_last_chars)
                            child.string = new_text
                    if child.parent:
                        process_siblings(child)
                i += 1

        process_siblings(soup)
        return str(soup).replace('\n', '').strip()

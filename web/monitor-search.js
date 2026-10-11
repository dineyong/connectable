/* Search only known catalog fields; every query token must match. */
(() => {
  const norm=s=>String(s ?? '').normalize('NFKC').toLowerCase().replace(/[·\-×]/g,'').replace(/\s+/g,'');
  window.monitorMatchesSearch=(p,query)=>{
    const f=p.filters || {};
    const specs=[];
    if(f.size!=null)specs.push(`${f.size}인치`,`${f.size}inch`);
    if(f.refresh!=null)specs.push(`${f.refresh}hz`);
    if(f.panel)specs.push(f.panel);
    if(f.width && f.height){
      specs.push(`${f.width}x${f.height}`,`${f.width}×${f.height}`);
      if(f.width===3840 && f.height===2160)specs.push('4k','uhd');
      if(f.width===2560 && f.height===1440)specs.push('qhd');
      if(f.width===1920 && f.height===1080)specs.push('fhd');
    }
    if(f.usb_c_video===true)specs.push('usb-c','usbc');
    const haystack=norm([p.manufacturer,p.display_model,...specs].join(' '));
    return String(query).trim().replace(/(\d)\s+(인치|inch|hz)/gi,'$1$2').split(/\s+/).filter(Boolean).every(token=>{
      const t=norm(token);
      const size=t.match(/^(\d+(?:\.\d+)?)(?:인치|inch)$/);
      if(size)return f.size!=null && Number(size[1])===f.size;
      const hz=t.match(/^(\d+(?:\.\d+)?)hz$/);
      if(hz)return f.refresh!=null && Number(hz[1])===f.refresh;
      if(['4k','uhd','qhd','fhd','usbc'].includes(t))return specs.some(s=>norm(s)===t);
      return haystack.includes(t);
    });
  };
})();

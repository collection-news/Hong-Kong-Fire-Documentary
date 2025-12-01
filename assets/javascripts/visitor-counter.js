/* 
   Wait for the DOM to be fully loaded.
   We also use a slight delay or check mechanism because MkDocs Material sometimes 
   manipulates the DOM or loads things via instant loading (if enabled), 
   which might wipe out our changes or mean the header isn't ready immediately.
*/

document.addEventListener("DOMContentLoaded", function() {
    initVisitorCounter();
});

/* 
   MkDocs Material uses 'instant loading' (PJAX-like) if enabled.
   We need to re-initialize the counter on navigation.
*/
// Listen for location changes if they happen (e.g. instant loading)
// Not strictly standard but often used in single page app contexts or with Material's instant loading
// We can also use a MutationObserver to be safe.

function initVisitorCounter() {
    // 1. Inject Busuanzi Script if not already present
    if (!document.getElementById("busuanzi-script")) {
        var script = document.createElement("script");
        script.id = "busuanzi-script";
        script.src = "//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js";
        script.async = true;
        document.body.appendChild(script);
    }

    // 2. Function to insert the counter
    function insertCounter() {
        var headerInner = document.querySelector(".md-header__inner");
        // Check if we already inserted it to avoid duplicates
        if (headerInner && !document.getElementById("busuanzi_container_site_pv_custom")) {
            var counter = document.createElement("div");
            counter.id = "busuanzi_container_site_pv_custom"; // Custom ID wrapper
            counter.className = "md-header__option";
            counter.style.marginLeft = "10px";
            counter.style.marginRight = "10px";
            counter.style.fontSize = "0.7rem";
            counter.style.color = "inherit";
            counter.style.whiteSpace = "nowrap";
            counter.style.display = "flex"; 
            counter.style.alignItems = "center";
            
            // Busuanzi looks for specific IDs. 
            // We use style="display:none" initially, Busuanzi will change it to inline.
            // We wrap it in our own container to ensure flex alignment works.
            counter.innerHTML = `
                <span id="busuanzi_container_site_pv" style="display:none">
                    Visitors: <span id="busuanzi_value_site_pv">--</span>
                </span>
            `;
            
            var search = document.querySelector(".md-search");
            var source = document.querySelector(".md-header__source");
            
            // Insert before source (repo link) or search
            if (source) {
                 headerInner.insertBefore(counter, source);
            } else if (search) {
                 headerInner.insertBefore(counter, search);
            } else {
                 headerInner.appendChild(counter);
            }
        }
    }

    // Run insertion immediately
    insertCounter();

    // 3. Observe header for changes (re-renders)
    var observer = new MutationObserver(function(mutations) {
        insertCounter();
    });
    
    var header = document.querySelector(".md-header");
    if (header) {
        observer.observe(header, { childList: true, subtree: true });
    }
}

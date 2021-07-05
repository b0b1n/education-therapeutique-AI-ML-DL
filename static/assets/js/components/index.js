function include(file) {
    const script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);
}

/* include all the components js file */

include("{% static 'assets/js/components/chat.js'%}");
include("{% static 'assets/js/constants.js'%}");
include("{% static 'assets/js/components/cardsCarousel.js'%}");
include("{% static 'assets/js/components/botTyping.js'%}");
include("{% static 'assets/js/components/charts.js'%}");
include("{% static 'assets/js/components/collapsible.js'%}");
include("{% static 'assets/js/components/dropDown.js'%}");
include("{% static 'assets/js/components/location.js'%}");
include("{% static 'assets/js/components/pdfAttachment.js'%}");
include("{% static 'assets/js/components/quickReplies.js'%}");
include("{% static 'assets/js/components/suggestionButtons.js'%}");
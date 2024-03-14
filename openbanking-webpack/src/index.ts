
import { Connect, ConnectEventHandlers, ConnectOptions, ConnectDoneEvent, ConnectCancelEvent, ConnectErrorEvent, ConnectRouteEvent } from 'connect-web-sdk';

// Ensure to replace this with the URL you get back from your call to the Generate Connect URL endpoint
const connectURL = 'https://connect2.finicity.com?customerId=7020734383&language=en&origin=url&partnerId=2445584469258&signature=edf15ff7e0bb8b1b635ec1251a63e86dccb4a1ae673b371cb8b2abcce2992a69&timestamp=1710264758853&ttl=1710271958853';

const connectEventHandlers: ConnectEventHandlers = {
    onDone: (event: ConnectDoneEvent) => { console.log(event); },
    onCancel: (event: ConnectCancelEvent) => { console.log(event); },
    onError: (event: ConnectErrorEvent) => { console.log(event); },
    onRoute: (event: ConnectRouteEvent) => { console.log(event); },
    onUser: (event: any) => { console.log(event); },
    onLoad: () => { console.log('loaded'); }
  };

  const connectOptions: ConnectOptions = {
    overlay: 'rgba(199,201,199, 0.5)'
  };

  Connect.launch(
    connectURL,
    connectEventHandlers,
    connectOptions
    );

// When you are finished with the Connect application don't forget to destroy it using the following call:
// FinicityConnect.destroy()
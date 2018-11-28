
declare var AWS: any;

export class ContentCollectorService {

    private AWS_KEY="";//"PUT KEY HERE"
    private AWS_SECRET="";//"PUT SECRET KEY HERE"
    private REGION="us-east-2"
    private doClient;
    private data_list: any[] = [];

    private setupAWS() {

        AWS.config.update({
            region: this.REGION,
            // accessKeyId default can be used while using the downloadable version of DynamoDB. 
            // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
            accessKeyId: this.AWS_KEY,
            // secretAccessKey default can be used while using the downloadable version of DynamoDB. 
            // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
            secretAccessKey: this.AWS_SECRET
        });

        this.doClient = new AWS.DynamoDB.DocumentClient();
    }

    private getMovieName(object: any) : any {
        for (var key in object) {
            if (key != "sentiment") {
                return key;
            }
        }
    }

    private getFavorite(sentiment_list: any) : any {

        //first we get the values for the initial item in the list
        var movieName: any = this.getMovieName(sentiment_list[0]);
        //we assume that this is the max until proven otherwise
        var maxAverageSentiment: number = Math.round(+(sentiment_list[0].sentiment) / +(sentiment_list[0][movieName]));

        //variables to hold the values we want to return
        var averageSentiment: number;
        var favorite = movieName;
        var sentiment: number = +(sentiment_list[0].sentiment);
        var favoriteCount: number = +(sentiment_list[0][movieName]);

        //loop to go through the list and determine which has the max average sentiment
        sentiment_list.forEach((movie) => {
            movieName = this.getMovieName(movie);
            averageSentiment = Math.round(+(movie.sentiment) / +(movie[movieName]));
            if (averageSentiment > maxAverageSentiment) {
                maxAverageSentiment = averageSentiment;
                favorite = movieName;
                sentiment = +(movie.sentiment);
                favoriteCount = +(movie[movieName]);
            }
        });

        return {
            favorite: favorite,
            sentiment: sentiment,
            averageSentiment: maxAverageSentiment,
            name: movieName,
            count: favoriteCount
        }
    }

    public getUsableData() : any{
        var returnList = [];
        var list_of_states = this.data_list;
        var favorite;

        list_of_states.forEach((state) => {
            favorite = this.getFavorite(state.list);
            returnList.push({
                state: state.state,
                movie: favorite.name,
                sentiment: favorite.sentiment,
                average: favorite.averageSentiment,
                count: favorite.count
            });
        });

        return returnList;
    }



    public constructor() {
        this.setupAWS();
    }

    public scanData(): any {

        var params = {
            TableName: "final_project"
        };

        var data_list: any[] = [];

        this.doClient.scan(params, (err, data) => {
            if (err) {
                console.log("something happened");
            } else {
                // Print all the movies
                console.log("Scan succeeded");
                data.Items.forEach((movie) => {
                    data_list.push(movie);
                });
            }
            this.data_list = data_list;
        });
    }
}
